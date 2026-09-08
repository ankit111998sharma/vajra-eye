package com.vajra.service;

import com.vajra.model.SceneObject;
import jakarta.annotation.PostConstruct;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfRect;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.opencv.objdetect.FaceDetectorYN;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Labels body parts the COCO detector does not name: face and hand.
 */
@Service
public class BodyPartDetector {

    private static final Logger log = LoggerFactory.getLogger(BodyPartDetector.class);

    private volatile FaceDetectorYN yunet;
    private volatile CascadeClassifier haar;
    private volatile boolean ready;

    @PostConstruct
    public void load() {
        Thread t = new Thread(this::loadInternal, "vajra-body-models");
        t.setDaemon(true);
        t.start();
    }

    private void loadInternal() {
        Path yunetPath = ModelCache.download(
                "face_detection_yunet_2023mar.onnx",
                "https://huggingface.co/opencv/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx",
                "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx");
        if (yunetPath != null) {
            try {
                yunet = FaceDetectorYN.create(yunetPath.toAbsolutePath().toString(), "",
                        new Size(320, 320), 0.55f, 0.3f, 5000);
                log.info("YuNet face detector ready");
            } catch (Exception e) {
                log.warn("YuNet not available ({})", e.getMessage());
            }
        }
        Path haarPath = ModelCache.download(
                "haarcascade_frontalface_default.xml",
                "https://raw.githubusercontent.com/opencv/opencv/4.9.0/data/haarcascades/haarcascade_frontalface_default.xml");
        if (haarPath != null) {
            CascadeClassifier cc = new CascadeClassifier(haarPath.toAbsolutePath().toString());
            if (!cc.empty()) {
                haar = cc;
                log.info("Haar face detector ready");
            }
        }
        ready = yunet != null || haar != null;
    }

    public boolean isReady() {
        return ready;
    }

    public List<SceneObject> detect(Mat frame, List<Rect> personBoxes) {
        List<SceneObject> out = new ArrayList<>();
        if (frame == null || frame.empty()) {
            return out;
        }
        List<Rect> faces = detectFaces(frame);
        for (Rect r : faces) {
            out.add(box("face", 0.80, r, false));
        }
        for (Rect r : detectHands(frame, personBoxes, faces)) {
            out.add(box("hand", 0.70, r, false));
        }
        return out;
    }

    private List<Rect> detectFaces(Mat frame) {
        List<Rect> faces = new ArrayList<>();
        if (yunet != null) {
            try {
                yunet.setInputSize(new Size(frame.cols(), frame.rows()));
                Mat detections = new Mat();
                yunet.detect(frame, detections);
                for (int i = 0; i < detections.rows(); i++) {
                    double[] row = detections.get(i, 0);
                    if (row == null || row.length < 5) {
                        continue;
                    }
                    int x = Math.max(0, (int) row[0]);
                    int y = Math.max(0, (int) row[1]);
                    int w = Math.max(8, (int) row[2]);
                    int h = Math.max(8, (int) row[3]);
                    faces.add(clip(frame, new Rect(x, y, w, h)));
                }
                detections.release();
                if (!faces.isEmpty()) {
                    return faces;
                }
            } catch (Exception e) {
                log.debug("YuNet face: {}", e.getMessage());
            }
        }
        if (haar != null && !haar.empty()) {
            Mat gray = new Mat();
            MatOfRect found = new MatOfRect();
            try {
                Imgproc.cvtColor(frame, gray, Imgproc.COLOR_BGR2GRAY);
                Imgproc.equalizeHist(gray, gray);
                haar.detectMultiScale(gray, found, 1.15, 5, 0, new Size(48, 48), new Size());
                for (Rect r : found.toArray()) {
                    faces.add(clip(frame, r));
                }
            } finally {
                gray.release();
                found.release();
            }
        }
        return faces;
    }

    private List<Rect> detectHands(Mat frame, List<Rect> personBoxes, List<Rect> faces) {
        List<Rect> hands = new ArrayList<>();
        Mat hsv = new Mat();
        Mat skin = new Mat();
        Mat skin2 = new Mat();
        try {
            Imgproc.cvtColor(frame, hsv, Imgproc.COLOR_BGR2HSV);
            Core.inRange(hsv, new Scalar(0, 30, 50), new Scalar(25, 180, 255), skin);
            Core.inRange(hsv, new Scalar(160, 30, 50), new Scalar(180, 180, 255), skin2);
            Core.bitwise_or(skin, skin2, skin);
            Imgproc.medianBlur(skin, skin, 7);
            Mat kernel = Imgproc.getStructuringElement(Imgproc.MORPH_ELLIPSE, new Size(5, 5));
            Imgproc.dilate(skin, skin, kernel);
            kernel.release();
            List<MatOfPoint> contours = new ArrayList<>();
            Mat hierarchy = new Mat();
            Imgproc.findContours(skin, contours, hierarchy, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
            hierarchy.release();
            List<Rect> candidates = new ArrayList<>();
            double frameArea = (double) frame.rows() * frame.cols();
            for (MatOfPoint c : contours) {
                double area = Imgproc.contourArea(c);
                Rect r = Imgproc.boundingRect(c);
                c.release();
                if (area < frameArea * 0.008 || area > frameArea * 0.06) {
                    continue;
                }
                double ar = r.width / (double) Math.max(1, r.height);
                if (ar < 0.4 || ar > 2.1) {
                    continue;
                }
                if (overlaps(r, faces, 0.40)) {
                    continue;
                }
                if (personBoxes != null && !personBoxes.isEmpty() && !overlaps(r, personBoxes, 0.20)) {
                    continue;
                }
                candidates.add(clip(frame, r));
            }
            candidates.sort((a, b) -> Integer.compare(b.width * b.height, a.width * a.height));
            for (int i = 0; i < Math.min(2, candidates.size()); i++) {
                hands.add(candidates.get(i));
            }
        } finally {
            hsv.release();
            skin.release();
            skin2.release();
        }
        return hands;
    }

    private static boolean overlaps(Rect r, List<Rect> others, double iouMin) {
        for (Rect o : others) {
            if (iou(r, o) >= iouMin) {
                return true;
            }
        }
        return false;
    }

    private static double iou(Rect a, Rect b) {
        int x1 = Math.max(a.x, b.x);
        int y1 = Math.max(a.y, b.y);
        int x2 = Math.min(a.x + a.width, b.x + b.width);
        int y2 = Math.min(a.y + a.height, b.y + b.height);
        int inter = Math.max(0, x2 - x1) * Math.max(0, y2 - y1);
        int union = a.width * a.height + b.width * b.height - inter;
        return union <= 0 ? 0 : inter / (double) union;
    }

    private static Rect clip(Mat frame, Rect r) {
        int x = Math.max(0, r.x);
        int y = Math.max(0, r.y);
        int w = Math.min(frame.cols() - x, r.width);
        int h = Math.min(frame.rows() - y, r.height);
        return new Rect(x, y, Math.max(1, w), Math.max(1, h));
    }

    private static SceneObject box(String name, double p, Rect r, boolean threat) {
        return new SceneObject(name, p, r.x, r.y, r.width, r.height, threat);
    }
}
