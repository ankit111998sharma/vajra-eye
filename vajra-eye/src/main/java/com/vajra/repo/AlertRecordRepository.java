package com.vajra.repo;

import com.vajra.entity.AlertRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface AlertRecordRepository extends JpaRepository<AlertRecord, Long> {
    Optional<AlertRecord> findByAlertCode(String alertCode);
    List<AlertRecord> findTop80ByOrderByCreatedAtDesc();
}
