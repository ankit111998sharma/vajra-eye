package com.vajra.service;

import com.vajra.entity.AlertRecord;
import com.vajra.entity.AppUser;
import com.vajra.entity.AuditRecord;
import com.vajra.entity.EvidenceRecord;
import com.vajra.entity.PolicySettings;
import com.vajra.repo.AlertRecordRepository;
import com.vajra.repo.AppUserRepository;
import com.vajra.repo.AuditRecordRepository;
import com.vajra.repo.EvidenceRecordRepository;
import com.vajra.repo.PolicySettingsRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class VajraDbService {

    private final AppUserRepository users;
    private final AlertRecordRepository alerts;
    private final EvidenceRecordRepository evidence;
    private final AuditRecordRepository audits;
    private final PolicySettingsRepository policies;

    public VajraDbService(AppUserRepository users,
                          AlertRecordRepository alerts,
                          EvidenceRecordRepository evidence,
                          AuditRecordRepository audits,
                          PolicySettingsRepository policies) {
        this.users = users;
        this.alerts = alerts;
        this.evidence = evidence;
        this.audits = audits;
        this.policies = policies;
    }

    @Transactional(readOnly = true)
    public Optional<AppUser> login(String username, String password) {
        if (username == null || password == null) {
            return Optional.empty();
        }
        return users.findByUsernameIgnoreCase(username.trim())
                .filter(u -> password.equals(u.getPassword()));
    }

    @Transactional
    public void ensureUser(String username, String password, String role, String displayName) {
        if (users.findByUsernameIgnoreCase(username).isPresent()) {
            return;
        }
        AppUser u = new AppUser();
        u.setUsername(username);
        u.setPassword(password);
        u.setRole(role);
        u.setDisplayName(displayName);
        users.save(u);
    }

    @Transactional
    public void saveAlert(String code, String weaponType, double confidence, String cameraId, String channel) {
        AlertRecord r = new AlertRecord();
        r.setAlertCode(code);
        r.setWeaponType(weaponType);
        r.setConfidence(confidence);
        r.setCameraId(cameraId);
        r.setChannel(channel);
        r.setAcked(false);
        r.setCreatedAt(Instant.now());
        alerts.save(r);
    }

    @Transactional
    public boolean ackAlert(String code) {
        Optional<AlertRecord> found = alerts.findByAlertCode(code);
        if (found.isEmpty()) {
            return false;
        }
        AlertRecord r = found.get();
        r.setAcked(true);
        alerts.save(r);
        return true;
    }

    @Transactional
    public void saveEvidence(String code, String cameraId, String kind, String note, long motionArea, byte[] jpeg) {
        EvidenceRecord r = evidence.findByEvidenceCode(code).orElseGet(EvidenceRecord::new);
        r.setEvidenceCode(code);
        r.setCameraId(cameraId);
        r.setKind(kind);
        r.setNote(note);
        r.setMotionArea(motionArea);
        r.setJpeg(jpeg);
        if (r.getCreatedAt() == null) {
            r.setCreatedAt(Instant.now());
        }
        evidence.save(r);
    }

    @Transactional(readOnly = true)
    public Optional<byte[]> evidenceJpeg(String code) {
        return evidence.findByEvidenceCode(code).map(EvidenceRecord::getJpeg);
    }

    @Transactional
    public void saveAudit(String username, String action, String detail) {
        AuditRecord r = new AuditRecord();
        r.setUsername(username);
        r.setAction(action);
        r.setDetail(detail != null && detail.length() > 500 ? detail.substring(0, 500) : detail);
        r.setCreatedAt(Instant.now());
        audits.save(r);
    }

    @Transactional
    public PolicySettings savePolicy(int pixel, double minArea, double pan, double pMin, long cooldown) {
        PolicySettings p = policies.findById(1L).orElseGet(PolicySettings::new);
        p.setId(1L);
        p.setPixelThreshold(pixel);
        p.setMinArea(minArea);
        p.setPanFraction(pan);
        p.setMinProbability(pMin);
        p.setCooldownMs(cooldown);
        return policies.save(p);
    }

    @Transactional
    public PolicySettings loadPolicy() {
        return policies.findById(1L).orElseGet(() -> {
            PolicySettings p = new PolicySettings();
            p.setId(1L);
            return policies.save(p);
        });
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> recentAlerts() {
        return alerts.findTop80ByOrderByCreatedAtDesc().stream().map(r -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("id", r.getAlertCode());
            m.put("weaponType", r.getWeaponType());
            m.put("confidence", r.getConfidence() == null ? 0 : r.getConfidence());
            m.put("cameraId", r.getCameraId());
            m.put("channel", r.getChannel());
            m.put("acked", r.isAcked());
            m.put("ts", r.getCreatedAt() == null ? Instant.now().toString() : r.getCreatedAt().toString());
            return m;
        }).toList();
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> recentEvidence() {
        return evidence.findTop24ByOrderByCreatedAtDesc().stream().map(r -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("id", r.getEvidenceCode());
            m.put("cameraId", r.getCameraId());
            m.put("kind", r.getKind());
            m.put("note", r.getNote());
            m.put("motionArea", r.getMotionArea());
            m.put("ts", r.getCreatedAt() == null ? Instant.now().toString() : r.getCreatedAt().toString());
            return m;
        }).toList();
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> recentAudit() {
        return audits.findTop120ByOrderByCreatedAtDesc().stream().map(r -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("id", "AU-" + r.getId());
            m.put("user", r.getUsername());
            m.put("action", r.getAction());
            m.put("detail", r.getDetail());
            m.put("ts", r.getCreatedAt() == null ? Instant.now().toString() : r.getCreatedAt().toString());
            return m;
        }).toList();
    }
}
