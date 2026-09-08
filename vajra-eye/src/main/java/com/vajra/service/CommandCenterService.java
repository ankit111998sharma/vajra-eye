package com.vajra.service;

import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.MatOfInt;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedDeque;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class CommandCenterService {

    private static final int MAX_ALERTS = 80;
    private static final int MAX_EVIDENCE = 24;
    private static final int MAX_AUDIT = 120;

    private final ConcurrentLinkedDeque<Map<String, Object>> alerts = new ConcurrentLinkedDeque<>();
    private final ConcurrentLinkedDeque<Map<String, Object>> evidence = new ConcurrentLinkedDeque<>();
    private final ConcurrentLinkedDeque<Map<String, Object>> audit = new ConcurrentLinkedDeque<>();
    private final ConcurrentHashMap<String, byte[]> evidenceJpeg = new ConcurrentHashMap<>();
    private final AtomicLong seq = new AtomicLong();
    private final VajraDbService db;
    private volatile long lastEvidencePersistMs;

    private volatile byte[] latestJpeg = new byte[0];

    public CommandCenterService(VajraDbService db) {
        this.db = db;
    }

    public void publishPreview(Mat frame, String cameraId, String state, boolean motion) {
        if (frame == null || frame.empty()) {
            return;
        }
        Mat vis = frame.clone();
        MatOfByte buf = new MatOfByte();
        try {
            String label = cameraId + "  |  " + state + (motion ? "  |  MOTION" : "  |  IDLE");
            Imgproc.rectangle(vis, new Point(8, 8), new Point(Math.min(vis.cols() - 8, 520), 42),
                    new Scalar(20, 24, 18), -1);
            Imgproc.putText(vis, label, new Point(16, 32),
                    Imgproc.FONT_HERSHEY_SIMPLEX, 0.55,
                    motion ? new Scalar(40, 40, 220) : new Scalar(200, 210, 180), 1, Imgproc.LINE_AA);
            Imgcodecs.imencode(".jpg", vis, buf, new MatOfInt(Imgcodecs.IMWRITE_JPEG_QUALITY, 72));
            latestJpeg = buf.toArray();
        } finally {
            vis.release();
            buf.release();
        }
    }

    public byte[] getLatestJpeg() {
        return latestJpeg;
    }

    public Map<String, Object> recordKeyframe(Mat frame, String cameraId, double approxArea) {
        String id = "KF-" + UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
        byte[] jpeg = encode(frame);
        if (jpeg.length > 0) {
            evidenceJpeg.put(id, jpeg);
        }
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("id", id);
        row.put("cameraId", cameraId);
        row.put("kind", "KEYFRAME");
        row.put("note", "Motion gate admitted frame");
        row.put("motionArea", Math.round(approxArea));
        row.put("ts", Instant.now().toString());
        evidence.addFirst(row);
        trim(evidence, MAX_EVIDENCE, "id");
        long now = System.currentTimeMillis();
        if (now - lastEvidencePersistMs >= 1000) {
            lastEvidencePersistMs = now;
            try {
                db.saveEvidence(id, cameraId, "KEYFRAME", "Motion gate admitted frame",
                        Math.round(approxArea), jpeg);
            } catch (Exception ignored) {
                // keep pipeline alive if MySQL is slow
            }
        }
        return row;
    }

    public Map<String, Object> recordAlert(String weaponType, double confidence, String cameraId, String channel) {
        String id = "AL-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("id", id);
        row.put("weaponType", weaponType);
        row.put("confidence", confidence);
        row.put("cameraId", cameraId);
        row.put("channel", channel);
        row.put("acked", false);
        row.put("ts", Instant.now().toString());
        alerts.addFirst(row);
        while (alerts.size() > MAX_ALERTS) {
            alerts.removeLast();
        }
        audit("SYSTEM", "ALERT", id + " " + weaponType);
        try {
            db.saveAlert(id, weaponType, confidence, cameraId, channel);
        } catch (Exception ignored) {
        }
        return row;
    }

    public boolean ack(String id, String user) {
        boolean memory = false;
        for (Map<String, Object> row : alerts) {
            if (id.equals(row.get("id"))) {
                row.put("acked", true);
                memory = true;
                break;
            }
        }
        boolean dbAck = false;
        try {
            dbAck = db.ackAlert(id);
        } catch (Exception ignored) {
        }
        if (memory || dbAck) {
            audit(user, "ACK_ALERT", id);
            return true;
        }
        return false;
    }

    public void audit(String user, String action, String detail) {
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("id", "AU-" + seq.incrementAndGet());
        row.put("user", user);
        row.put("action", action);
        row.put("detail", detail);
        row.put("ts", Instant.now().toString());
        audit.addFirst(row);
        while (audit.size() > MAX_AUDIT) {
            audit.removeLast();
        }
        try {
            db.saveAudit(user, action, detail);
        } catch (Exception ignored) {
        }
    }

    public List<Map<String, Object>> alerts() {
        Map<String, Map<String, Object>> byId = new LinkedHashMap<>();
        for (Map<String, Object> row : alerts) {
            Object id = row.get("id");
            if (id != null) {
                byId.put(id.toString(), row);
            }
        }
        try {
            for (Map<String, Object> row : db.recentAlerts()) {
                Object id = row.get("id");
                if (id != null) {
                    byId.putIfAbsent(id.toString(), row);
                }
            }
        } catch (Exception ignored) {
        }
        List<Map<String, Object>> out = new ArrayList<>(byId.values());
        out.sort((a, b) -> String.valueOf(b.getOrDefault("ts", ""))
                .compareTo(String.valueOf(a.getOrDefault("ts", ""))));
        return out;
    }

    public List<Map<String, Object>> evidence() {
        try {
            List<Map<String, Object>> fromDb = db.recentEvidence();
            if (!fromDb.isEmpty()) {
                return fromDb;
            }
        } catch (Exception ignored) {
        }
        return new ArrayList<>(evidence);
    }

    public List<Map<String, Object>> auditLog() {
        try {
            List<Map<String, Object>> fromDb = db.recentAudit();
            if (!fromDb.isEmpty()) {
                return fromDb;
            }
        } catch (Exception ignored) {
        }
        return new ArrayList<>(audit);
    }

    public byte[] evidenceJpeg(String id) {
        byte[] mem = evidenceJpeg.get(id);
        if (mem != null && mem.length > 0) {
            return mem;
        }
        try {
            return db.evidenceJpeg(id).orElse(new byte[0]);
        } catch (Exception e) {
            return new byte[0];
        }
    }

    private byte[] encode(Mat frame) {
        if (frame == null || frame.empty()) {
            return new byte[0];
        }
        MatOfByte buf = new MatOfByte();
        try {
            Imgcodecs.imencode(".jpg", frame, buf, new MatOfInt(Imgcodecs.IMWRITE_JPEG_QUALITY, 70));
            return buf.toArray();
        } finally {
            buf.release();
        }
    }

    private void trim(ConcurrentLinkedDeque<Map<String, Object>> deque, int max, String idKey) {
        while (deque.size() > max) {
            Map<String, Object> old = deque.removeLast();
            Object id = old.get(idKey);
            if (id != null) {
                evidenceJpeg.remove(id.toString());
            }
        }
    }
}
