package com.vajra.service;

import com.vajra.model.SceneObject;
import com.vajra.model.ThreatEvent;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class VideoProcessor {

    private static final Logger log = LoggerFactory.getLogger(VideoProcessor.class);

    private final MotionDetectionService motionService;
    private final DetectionService detectionService;
    private final AlertService alertService;
    private final AlertDebounceManager debounce;
    private final FrameBufferQueue queue;
    private final StatusHolder status;
    private final CommandCenterService commandCenter;

    @Value("${vajra.video.source:0}")
    private String videoSource;

    @Value("${vajra.camera.id:CAM-LAB-01}")
    private String cameraId;

    @Value("${vajra.detect.min-probability:0.20}")
    private double minProbability;

    @Value("${vajra.demo.synthetic:true}")
    private boolean allowSynthetic;

    private final AtomicBoolean running = new AtomicBoolean(false);
    private final AtomicBoolean capturing = new AtomicBoolean(true);
    private Thread captureThread;
    private Thread workerThread;

    public VideoProcessor(MotionDetectionService motionService,
                          DetectionService detectionService,
                          AlertService alertService,
                          AlertDebounceManager debounce,
                          FrameBufferQueue queue,
                          StatusHolder status,
                          CommandCenterService commandCenter) {
        this.motionService = motionService;
        this.detectionService = detectionService;
        this.alertService = alertService;
        this.debounce = debounce;
        this.queue = queue;
        this.status = status;
        this.commandCenter = commandCenter;
    }

    @PostConstruct
    public void start() {
        running.set(true);
        captureThread = new Thread(this::captureLoop, "vajra-capture");
        workerThread = new Thread(this::workerLoop, "vajra-worker");
        captureThread.setDaemon(true);
        workerThread.setDaemon(true);
        captureThread.start();
        workerThread.start();
        capturing.set(true);
        status.setState("CAPTURING");
        log.info("VAJRA-EYE pipeline threads started. source={}", videoSource);
    }

    public synchronized void startCapture() {
        capturing.set(true);
        motionService.resetBaseline();
        status.setLastMotion(false);
        status.setState("CAPTURING");
        log.info("Capture START requested");
    }

    public synchronized void stopCapture() {
        capturing.set(false);
        status.setLastMotion(false);
        status.setState("STOPPED");
        queue.drainAndRelease();
        motionService.resetBaseline();
        log.info("Capture STOP requested");
    }

    public boolean isCapturing() {
        return capturing.get();
    }

    @PreDestroy
    public void stop() {
        running.set(false);
        queue.drainAndRelease();
    }

    private void captureLoop() {
        int failures = 0;
        while (running.get()) {
            if (!capturing.get()) {
                status.setState("STOPPED");
                sleep(200);
                continue;
            }
            VideoCapture capture = openSource();
            if (capture == null || !capture.isOpened()) {
                failures++;
                long backoff = Math.min(10_000, 1_000L * (1L << Math.min(failures, 4)));
                log.warn("Video source unavailable. Reconnect in {} ms (#{})", backoff, failures);
                status.setState("RECONNECTING");
                if (allowSynthetic && capturing.get()) {
                    pushSyntheticBurst();
                }
                sleep(backoff);
                continue;
            }
            failures = 0;
            motionService.resetBaseline();
            capture.set(Videoio.CAP_PROP_BUFFERSIZE, 1);
            status.setState("CAPTURING");
            log.info("Video source opened: {}", videoSource);
            Mat frame = new Mat();
            try {
                while (running.get() && capturing.get() && capture.read(frame)) {
                    if (frame.empty()) {
                        break;
                    }
                    Mat copy = frame.clone();
                    if (!queue.pushFrame(copy)) {
                        copy.release();
                    }
                    status.incrementFrames();
                }
            } finally {
                frame.release();
                capture.release();
            }
        }
    }

    private VideoCapture openSource() {
        try {
            if (videoSource == null || videoSource.isBlank()) {
                return null;
            }
            if (videoSource.chars().allMatch(Character::isDigit)) {
                return new VideoCapture(Integer.parseInt(videoSource));
            }
            return new VideoCapture(videoSource);
        } catch (Exception e) {
            log.warn("openSource failed: {}", e.getMessage());
            return null;
        }
    }

    private void pushSyntheticBurst() {
        status.setState("SYNTHETIC_DEMO");
        for (int i = 0; i < 40 && running.get(); i++) {
            Mat frame = syntheticFrame(i);
            if (!queue.pushFrame(frame)) {
                frame.release();
            }
            status.incrementFrames();
            sleep(40);
        }
    }

    private Mat syntheticFrame(int t) {
        Mat frame = Mat.zeros(480, 640, org.opencv.core.CvType.CV_8UC3);
        frame.setTo(new Scalar(32, 40, 28));
        int x = 40 + (t * 12) % 500;
        Imgproc.rectangle(frame, new Point(x, 180), new Point(x + 90, 320), new Scalar(20, 20, 180), -1);
        Imgproc.putText(frame, "VAJRA-EYE SYNTHETIC", new Point(12, 28),
                Imgproc.FONT_HERSHEY_SIMPLEX, 0.7, new Scalar(220, 220, 220), 2);
        return frame;
    }

    private void workerLoop() {
        while (running.get()) {
            Mat frame = null;
            try {
                frame = queue.popFrame(500);
                if (frame == null) {
                    continue;
                }
                if (!capturing.get()) {
                    continue;
                }
                boolean motion = motionService.detectMotion(frame);
                status.setLastMotion(motion);
                if (motion) {
                    status.incrementKeyframes();
                    commandCenter.recordKeyframe(frame, cameraId, motionService.getLastMotionArea());
                }
                List<SceneObject> detections = detectionService.detectAll(frame);
                drawDetections(frame, detections);
                commandCenter.publishPreview(frame, cameraId, status.getState(), motion);
                for (SceneObject obj : detections) {
                    String raw = obj.getClassName();
                    double p = obj.getProbability();
                    if (!WeaponCatalog.shouldAlert(raw, p, minProbability)) {
                        continue;
                    }
                    String weapon = WeaponCatalog.lookup(raw);
                    ThreatEvent event = new ThreatEvent(weapon, p, cameraId, "lab");
                    if (debounce.shouldDispatch(event)) {
                        log.warn("Human-harming weapon on camera: {} p={}", weapon, p);
                        alertService.sendAlert(event);
                        status.incrementAlerts();
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            } catch (Exception e) {
                log.warn("Worker cycle failed: {}", e.getMessage());
            } finally {
                if (frame != null) {
                    frame.release();
                }
            }
        }
    }

    private void drawDetections(Mat frame, List<SceneObject> detections) {
        if (frame == null || frame.empty() || detections == null) {
            return;
        }
        int h = frame.rows();
        int row = 0;
        for (SceneObject obj : detections) {
            boolean threat = obj.isThreat();
            Scalar color = threat ? new Scalar(0, 0, 255) : new Scalar(80, 200, 80);
            if (obj.getW() > 2 && obj.getH() > 2) {
                Imgproc.rectangle(frame,
                        new Point(obj.getX(), obj.getY()),
                        new Point(obj.getX() + obj.getW(), obj.getY() + obj.getH()),
                        color, 2);
            }
            String label = obj.getClassName() + String.format(" %.2f", obj.getProbability());
            if (threat) {
                label = "ALERT " + label;
            }
            Imgproc.putText(frame, label, new Point(12, Math.min(h - 8, 64 + row * 22)),
                    Imgproc.FONT_HERSHEY_SIMPLEX, 0.55, color, 2);
            row++;
        }
    }

    private void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Service
    public static class StatusHolder {
        private volatile String state = "STARTING";
        private volatile boolean lastMotion;
        private final AtomicLong frames = new AtomicLong();
        private final AtomicLong keyframes = new AtomicLong();
        private final AtomicLong alerts = new AtomicLong();

        public String getState() {
            return state;
        }

        public void setState(String state) {
            this.state = state;
        }

        public boolean isLastMotion() {
            return lastMotion;
        }

        public void setLastMotion(boolean lastMotion) {
            this.lastMotion = lastMotion;
        }

        public void incrementFrames() {
            frames.incrementAndGet();
        }

        public void incrementKeyframes() {
            keyframes.incrementAndGet();
        }

        public void incrementAlerts() {
            alerts.incrementAndGet();
        }

        public long getFrames() {
            return frames.get();
        }

        public long getKeyframes() {
            return keyframes.get();
        }

        public long getAlerts() {
            return alerts.get();
        }
    }

    public String getCameraId() {
        return cameraId;
    }

    public String getVideoSource() {
        return videoSource;
    }

    public double getMinProbability() {
        return minProbability;
    }

    public void setMinProbability(double minProbability) {
        this.minProbability = minProbability;
    }
}
