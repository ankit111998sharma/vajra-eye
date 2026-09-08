package com.vajra.repo;

import com.vajra.entity.AuditRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AuditRecordRepository extends JpaRepository<AuditRecord, Long> {
    List<AuditRecord> findTop120ByOrderByCreatedAtDesc();
}
