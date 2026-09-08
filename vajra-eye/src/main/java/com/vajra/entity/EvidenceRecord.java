package com.vajra.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.Instant;

@Entity
@Table(name = "evidence_record")
public class EvidenceRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "evidence_code", nullable = false, unique = true, length = 64)
    private String evidenceCode;

    @Column(name = "camera_id", length = 80)
    private String cameraId;

    @Column(length = 40)
    private String kind;

    @Column(length = 200)
    private String note;

    @Column(name = "motion_area")
    private Long motionArea;

    @JdbcTypeCode(SqlTypes.VARBINARY)
    @Column(name = "jpeg", columnDefinition = "LONGBLOB")
    private byte[] jpeg;

    @Column(name = "created_at")
    private Instant createdAt;

    @PrePersist
    public void onCreate() {
        if (createdAt == null) {
            createdAt = Instant.now();
        }
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEvidenceCode() {
        return evidenceCode;
    }

    public void setEvidenceCode(String evidenceCode) {
        this.evidenceCode = evidenceCode;
    }

    public String getCameraId() {
        return cameraId;
    }

    public void setCameraId(String cameraId) {
        this.cameraId = cameraId;
    }

    public String getKind() {
        return kind;
    }

    public void setKind(String kind) {
        this.kind = kind;
    }

    public String getNote() {
        return note;
    }

    public void setNote(String note) {
        this.note = note;
    }

    public Long getMotionArea() {
        return motionArea;
    }

    public void setMotionArea(Long motionArea) {
        this.motionArea = motionArea;
    }

    public byte[] getJpeg() {
        return jpeg;
    }

    public void setJpeg(byte[] jpeg) {
        this.jpeg = jpeg;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}
