package com.vajra.model;

import java.time.Instant;

public class ThreatEvent {

    private String weaponType;
    private double confidence;
    private String cameraId;
    private String location;
    private Instant timestamp;

    public ThreatEvent() {
    }

    public ThreatEvent(String weaponType, double confidence, String cameraId, String location) {
        this.weaponType = weaponType;
        this.confidence = confidence;
        this.cameraId = cameraId;
        this.location = location;
        this.timestamp = Instant.now();
    }

    public String getWeaponType() {
        return weaponType;
    }

    public void setWeaponType(String weaponType) {
        this.weaponType = weaponType;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getCameraId() {
        return cameraId;
    }

    public void setCameraId(String cameraId) {
        this.cameraId = cameraId;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "ThreatEvent{" +
                "weaponType='" + weaponType + '\'' +
                ", confidence=" + confidence +
                ", cameraId='" + cameraId + '\'' +
                ", ts=" + timestamp +
                '}';
    }
}
