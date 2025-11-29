# 리포트 전송 이력 저장 구현

- **Type**: Functional
- **Key**: BE-DELIVERY-001
- **REQ / Epic**: REQ-FUNC-028
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

리포트 전송 이력을 데이터베이스에 저장하는 기능을 구현합니다. 누구에게, 언제 전송했는지 추적할 수 있습니다.

## ✅ Acceptance Criteria

### Entity 및 Repository
- [ ] `ReportDelivery` 엔티티 생성
- [ ] `ReportDeliveryRepository` 생성

### Service 구현
- [ ] `ReportDeliveryService` 클래스 생성
- [ ] `saveDeliveryHistory()` 메서드 구현

### 저장 정보
- [ ] 리포트 ID, 수신자 이메일, 전송 시간
- [ ] 전송 상태 (SUCCESS, FAILED)
- [ ] 실패 사유 (있는 경우)

### 테스트
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### ReportDelivery.java

```java
package com.reacademix.reacademix_backend.domain.delivery;

import com.reacademix.reacademix_backend.domain.BaseTimeEntity;
import com.reacademix.reacademix_backend.domain.report.Report;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "report_deliveries")
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReportDelivery extends BaseTimeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "report_id", nullable = false)
    private Report report;

    @Column(name = "recipient_email", nullable = false)
    private String recipientEmail;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private DeliveryStatus status;

    @Column(name = "failure_reason")
    private String failureReason;

    @Column(name = "sent_at")
    private java.time.LocalDateTime sentAt;

    public void markAsSent() {
        this.status = DeliveryStatus.SUCCESS;
        this.sentAt = java.time.LocalDateTime.now();
    }

    public void markAsFailed(String reason) {
        this.status = DeliveryStatus.FAILED;
        this.failureReason = reason;
    }
}
```

### DeliveryStatus.java

```java
package com.reacademix.reacademix_backend.domain.delivery;

public enum DeliveryStatus {
    PENDING,
    SUCCESS,
    FAILED
}
```

### ReportDeliveryService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.delivery.DeliveryStatus;
import com.reacademix.reacademix_backend.domain.delivery.ReportDelivery;
import com.reacademix.reacademix_backend.domain.report.Report;
import com.reacademix.reacademix_backend.repository.ReportDeliveryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class ReportDeliveryService {

    private final ReportDeliveryRepository deliveryRepository;

    @Transactional
    public ReportDelivery saveDeliveryHistory(Report report, String recipientEmail, boolean success, String failureReason) {
        log.info("전송 이력 저장: reportId={}, email={}, success={}", 
            report.getId(), recipientEmail, success);

        ReportDelivery delivery = ReportDelivery.builder()
            .report(report)
            .recipientEmail(recipientEmail)
            .status(success ? DeliveryStatus.SUCCESS : DeliveryStatus.FAILED)
            .failureReason(success ? null : failureReason)
            .sentAt(success ? java.time.LocalDateTime.now() : null)
            .build();

        return deliveryRepository.save(delivery);
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-09
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-028
- Related Epic: Report Delivery
