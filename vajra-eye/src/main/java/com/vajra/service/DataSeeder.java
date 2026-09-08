package com.vajra.service;

import com.vajra.entity.PolicySettings;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class DataSeeder implements ApplicationRunner {

    private final VajraDbService db;
    private final MotionDetectionService motion;
    private final VideoProcessor video;
    private final AlertDebounceManager debounce;

    public DataSeeder(VajraDbService db,
                      MotionDetectionService motion,
                      VideoProcessor video,
                      AlertDebounceManager debounce) {
        this.db = db;
        this.motion = motion;
        this.video = video;
        this.debounce = debounce;
    }

    @Override
    public void run(ApplicationArguments args) {
        db.ensureUser("localhost", "root", "ADMIN", "MySQL Workbench admin");
        db.ensureUser("root", "root", "ADMIN", "Root administrator");
        db.ensureUser("admin", "vajra", "ADMIN", "Lab administrator");
        db.ensureUser("operator", "vajra", "FIELD_USER", "Field operator");
        db.ensureUser("cmd", "vajra", "CMD_OFFICER", "Command officer");
        PolicySettings p = db.loadPolicy();
        if (p.getPixelThreshold() != null) {
            motion.setPixelThreshold(p.getPixelThreshold());
        }
        if (p.getMinArea() != null) {
            motion.setMinArea(p.getMinArea());
        }
        if (p.getPanFraction() != null) {
            motion.setPanFraction(p.getPanFraction());
        }
        if (p.getMinProbability() != null && p.getMinProbability() <= 0.35) {
            video.setMinProbability(p.getMinProbability());
        } else {
            video.setMinProbability(0.20);
        }
        if (p.getCooldownMs() != null) {
            debounce.setCooldownMs(p.getCooldownMs());
        }
        db.saveAudit("system", "BOOT", "Database seeded; policy loaded");
    }
}
