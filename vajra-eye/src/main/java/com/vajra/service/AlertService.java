package com.vajra.service;

import com.vajra.model.ThreatEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class AlertService {

    private static final Logger log = LoggerFactory.getLogger(AlertService.class);
    private static final int GCM_TAG_BITS = 128;
    private static final int IV_LEN = 12;

    @Value("${vajra.alert.key:VajraEyeLabKeyChangeMe!!}")
    private String keyMaterial;

    @Value("${twilio.account.sid:}")
    private String twilioSid;

    @Value("${twilio.auth.token:}")
    private String twilioToken;

    @Value("${twilio.phone.number:}")
    private String twilioFrom;

    @Value("${vajra.alert.sms.to:}")
    private String smsTo;

    private final AtomicLong alertCount = new AtomicLong();
    private final SecureRandom random = new SecureRandom();
    private final CommandCenterService commandCenter;

    public AlertService(CommandCenterService commandCenter) {
        this.commandCenter = commandCenter;
    }

    public long getAlertCount() {
        return alertCount.get();
    }

    public void sendAlert(ThreatEvent event) {
        String channel = (twilioSid == null || twilioSid.isBlank()) ? "LOG" : "SMS";
        try {
            commandCenter.recordAlert(event.getWeaponType(), event.getConfidence(),
                    event.getCameraId(), channel);
        } catch (Exception e) {
            log.error("Alert record failed: {}", e.getMessage());
        }
        try {
            String encrypted = encrypt(event.toString());
            alertCount.incrementAndGet();
            log.warn("ALERT sent for human-harming weapon: class={} p={} camera={} channel={}",
                    event.getWeaponType(), event.getConfidence(), event.getCameraId(), channel);
            dispatchSmsIfConfigured(encrypted);
        } catch (Exception e) {
            log.error("Alert encryption/dispatch failed: {}", e.getMessage());
        }
    }

    private void dispatchSmsIfConfigured(String body) {
        if (twilioSid == null || twilioSid.isBlank() || smsTo == null || smsTo.isBlank()) {
            log.info("Twilio not configured; alert retained in log only (laboratory mode).");
            return;
        }
        try {
            com.twilio.Twilio.init(twilioSid, twilioToken);
            com.twilio.rest.api.v2010.account.Message.creator(
                    new com.twilio.type.PhoneNumber(smsTo),
                    new com.twilio.type.PhoneNumber(twilioFrom),
                    body
            ).create();
        } catch (Exception e) {
            log.error("SMS dispatch failed: {}", e.getMessage());
        }
    }

    public String encrypt(String data) throws Exception {
        byte[] keyBytes = MessageDigest.getInstance("SHA-256")
                .digest(keyMaterial.getBytes(StandardCharsets.UTF_8));
        SecretKey key = new SecretKeySpec(keyBytes, "AES");
        byte[] iv = new byte[IV_LEN];
        random.nextBytes(iv);
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(GCM_TAG_BITS, iv));
        byte[] cipherText = cipher.doFinal(data.getBytes(StandardCharsets.UTF_8));
        byte[] packed = new byte[iv.length + cipherText.length];
        System.arraycopy(iv, 0, packed, 0, iv.length);
        System.arraycopy(cipherText, 0, packed, iv.length, cipherText.length);
        return Base64.getEncoder().encodeToString(packed);
    }
}
