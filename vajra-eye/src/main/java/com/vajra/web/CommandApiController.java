package com.vajra.web;

import com.vajra.service.AlertDebounceManager;
import com.vajra.service.CommandCenterService;
import com.vajra.service.DetectionService;
import com.vajra.service.MotionDetectionService;
import com.vajra.service.AuthService;
import com.vajra.service.VajraDbService;
import com.vajra.service.WeaponCatalog;
import jakarta.servlet.http.HttpSession;
import com.vajra.service.VideoProcessor;
import com.vajra.service.VideoProcessor.StatusHolder;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CommandApiController {

    private final StatusHolder status;
    private final DetectionService detectionService;
    private final CommandCenterService commandCenter;
    private final MotionDetectionService motionService;
    private final VideoProcessor videoProcessor;
    private final AlertDebounceManager debounce;
    private final VajraDbService db;
    private final AuthService auth;

    public CommandApiController(StatusHolder status,
                                DetectionService detectionService,
                                CommandCenterService commandCenter,
                                MotionDetectionService motionService,
                                VideoProcessor videoProcessor,
                                AlertDebounceManager debounce,
                                VajraDbService db,
                                AuthService auth) {
        this.status = status;
        this.detectionService = detectionService;
        this.commandCenter = commandCenter;
        this.motionService = motionService;
        this.videoProcessor = videoProcessor;
        this.debounce = debounce;
        this.db = db;
        this.auth = auth;
    }

    @GetMapping("/status")
    public Map<String, Object> pipeline() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("service", "VAJRA-EYE");
        m.put("pipeline", status.getState());
        m.put("modelReady", detectionService.isModelReady());
        m.put("detector", detectionService.getEngineLabel());
        m.put("detectorError", detectionService.getLastError());
        m.put("seen", detectionService.getLastSeen());
        m.put("alertPolicy", "Alert only if a weapon that can harm a living human is detected");
        m.put("lastMotion", status.isLastMotion());
        m.put("lastMotionArea", motionService.getLastMotionArea());
        m.put("framesIngested", status.getFrames());
        m.put("keyframes", status.getKeyframes());
        m.put("alerts", status.getAlerts());
        m.put("cameraId", videoProcessor.getCameraId());
        m.put("videoSource", videoProcessor.getVideoSource());
        m.put("capturing", videoProcessor.isCapturing());
        m.put("ts", Instant.now().toString());
        return m;
    }

    @PostMapping("/capture/start")
    public Map<String, Object> startCapture(HttpSession session) {
        videoProcessor.startCapture();
        Object user = session.getAttribute("username");
        commandCenter.audit(user == null ? "operator" : user.toString(), "CAPTURE_START", "Motion capture started");
        return pipeline();
    }

    @PostMapping("/capture/stop")
    public Map<String, Object> stopCapture(HttpSession session) {
        videoProcessor.stopCapture();
        Object user = session.getAttribute("username");
        commandCenter.audit(user == null ? "operator" : user.toString(), "CAPTURE_STOP", "Motion capture stopped");
        return pipeline();
    }

    @GetMapping(value = "/snapshot.jpg", produces = MediaType.IMAGE_JPEG_VALUE)
    public ResponseEntity<byte[]> snapshot() {
        byte[] jpg = commandCenter.getLatestJpeg();
        if (jpg == null || jpg.length == 0) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok()
                .cacheControl(org.springframework.http.CacheControl.noStore())
                .body(jpg);
    }

    @GetMapping("/alerts")
    public Map<String, Object> alerts() {
        Map<String, Object> m = new LinkedHashMap<>();
        List<Map<String, Object>> items = commandCenter.alerts();
        m.put("items", items == null ? List.of() : items);
        m.put("weapons", WeaponCatalog.listing());
        m.put("modelReady", detectionService.isModelReady());
        m.put("detector", detectionService.getEngineLabel());
        m.put("seen", detectionService.getLastSeen());
        m.put("detectorError", detectionService.getLastError());
        m.put("policy", "An alert is sent only when the camera detects a weapon that can harm a living human.");
        return m;
    }

    @GetMapping("/weapons")
    public Map<String, Object> weapons() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("items", WeaponCatalog.listing());
        m.put("nowOnThisCamera", List.of("person", "face", "hand", "knife", "scissors", "fork", "baseball bat"));
        m.put("modelReady", detectionService.isModelReady());
        m.put("detector", detectionService.getEngineLabel());
        m.put("seen", detectionService.getLastSeen());
        m.put("policy", "An alert is sent only when the camera detects a weapon that can harm a living human.");
        return m;
    }

    @PostMapping("/alerts/{id}/ack")
    public Map<String, Object> ack(@PathVariable String id, @RequestBody(required = false) Map<String, String> body) {
        String user = body != null ? body.getOrDefault("user", "operator") : "operator";
        boolean ok = commandCenter.ack(id, user);
        return Map.of("ok", ok, "id", id);
    }

    @GetMapping("/evidence")
    public Map<String, Object> evidence() {
        return Map.of("items", commandCenter.evidence());
    }

    @GetMapping(value = "/evidence/{id}.jpg", produces = MediaType.IMAGE_JPEG_VALUE)
    public ResponseEntity<byte[]> evidenceJpeg(@PathVariable String id) {
        byte[] jpg = commandCenter.evidenceJpeg(id);
        if (jpg == null || jpg.length == 0) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok().body(jpg);
    }

    @GetMapping("/audit")
    public Map<String, Object> audit() {
        return Map.of("items", commandCenter.auditLog());
    }

    @GetMapping("/config")
    public Map<String, Object> config() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("pixelThreshold", motionService.getPixelThreshold());
        m.put("minArea", motionService.getMinArea());
        m.put("panFraction", motionService.getPanFraction());
        m.put("minProbability", videoProcessor.getMinProbability());
        m.put("cooldownMs", debounce.getCooldownMs());
        m.put("cameraId", videoProcessor.getCameraId());
        return m;
    }

    @PostMapping("/config")
    public Map<String, Object> saveConfig(@RequestBody Map<String, Object> body) {
        if (body.get("pixelThreshold") != null) {
            motionService.setPixelThreshold(((Number) body.get("pixelThreshold")).intValue());
        }
        if (body.get("minArea") != null) {
            motionService.setMinArea(((Number) body.get("minArea")).doubleValue());
        }
        if (body.get("panFraction") != null) {
            motionService.setPanFraction(((Number) body.get("panFraction")).doubleValue());
        }
        if (body.get("minProbability") != null) {
            videoProcessor.setMinProbability(((Number) body.get("minProbability")).doubleValue());
        }
        if (body.get("cooldownMs") != null) {
            debounce.setCooldownMs(((Number) body.get("cooldownMs")).longValue());
        }
        String user = String.valueOf(body.getOrDefault("user", "admin"));
        db.savePolicy(
                motionService.getPixelThreshold(),
                motionService.getMinArea(),
                motionService.getPanFraction(),
                videoProcessor.getMinProbability(),
                debounce.getCooldownMs());
        commandCenter.audit(user, "UPDATE_POLICY", "Policy saved to MySQL");
        return config();
    }

    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody(required = false) Map<String, String> body, HttpSession session) {
        String user = body == null ? "" : body.getOrDefault("username", "").trim();
        String pass = body == null ? "" : body.getOrDefault("password", "");
        Map<String, Object> m = new LinkedHashMap<>();
        return auth.authenticate(user, pass).map(u -> {
            session.setAttribute("username", u.getUsername());
            session.setAttribute("role", u.getRole());
            session.setAttribute("displayName", u.getDisplayName());
            try {
                commandCenter.audit(u.getUsername(), "LOGIN", u.getRole());
            } catch (Exception ignored) {
            }
            m.put("ok", true);
            m.put("username", u.getUsername());
            m.put("role", u.getRole());
            m.put("displayName", u.getDisplayName());
            return m;
        }).orElseGet(() -> {
            m.put("ok", false);
            m.put("error", "Invalid credentials. Use username localhost and password root.");
            return m;
        });
    }
}
