package com.vajra.service;

import com.vajra.model.ThreatEvent;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.concurrent.ConcurrentHashMap;

@Service
public class AlertDebounceManager {

    private final ConcurrentHashMap<String, Long> lastDispatchedTimes = new ConcurrentHashMap<>();

    @Value("${vajra.alert.cooldown-ms:15000}")
    private long cooldownMs;

    public boolean shouldDispatch(ThreatEvent threat) {
        long now = System.currentTimeMillis();
        String key = threat.getCameraId() + "|" + threat.getWeaponType();
        Long last = lastDispatchedTimes.get(key);
        if (last == null || (now - last) > cooldownMs) {
            lastDispatchedTimes.put(key, now);
            return true;
        }
        return false;
    }

    public long getCooldownMs() {
        return cooldownMs;
    }

    public void setCooldownMs(long cooldownMs) {
        this.cooldownMs = cooldownMs;
    }
}
