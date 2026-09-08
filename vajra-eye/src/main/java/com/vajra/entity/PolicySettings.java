package com.vajra.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "policy_settings")
public class PolicySettings {

    @Id
    private Long id = 1L;

    @Column(name = "pixel_threshold")
    private Integer pixelThreshold = 25;

    @Column(name = "min_area")
    private Double minArea = 1000.0;

    @Column(name = "pan_fraction")
    private Double panFraction = 0.60;

    @Column(name = "min_probability")
    private Double minProbability = 0.20;

    @Column(name = "cooldown_ms")
    private Long cooldownMs = 15000L;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getPixelThreshold() {
        return pixelThreshold;
    }

    public void setPixelThreshold(Integer pixelThreshold) {
        this.pixelThreshold = pixelThreshold;
    }

    public Double getMinArea() {
        return minArea;
    }

    public void setMinArea(Double minArea) {
        this.minArea = minArea;
    }

    public Double getPanFraction() {
        return panFraction;
    }

    public void setPanFraction(Double panFraction) {
        this.panFraction = panFraction;
    }

    public Double getMinProbability() {
        return minProbability;
    }

    public void setMinProbability(Double minProbability) {
        this.minProbability = minProbability;
    }

    public Long getCooldownMs() {
        return cooldownMs;
    }

    public void setCooldownMs(Long cooldownMs) {
        this.cooldownMs = cooldownMs;
    }
}
