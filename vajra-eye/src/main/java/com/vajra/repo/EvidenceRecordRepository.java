package com.vajra.repo;

import com.vajra.entity.EvidenceRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface EvidenceRecordRepository extends JpaRepository<EvidenceRecord, Long> {
    Optional<EvidenceRecord> findByEvidenceCode(String evidenceCode);
    List<EvidenceRecord> findTop24ByOrderByCreatedAtDesc();
}
