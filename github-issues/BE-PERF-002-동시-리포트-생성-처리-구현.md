# 동시 리포트 생성 처리 구현

- **Type**: Non-Functional
- **Key**: BE-PERF-002
- **REQ / Epic**: REQ-NF-004
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-REPORT-003

## 📌 Description

최대 10건의 동시 리포트 생성을 처리하고, 초과 요청은 대기열에 추가하는 기능을 구현합니다.

## ✅ Acceptance Criteria

### 동시 처리 제한
- [ ] 최대 10건 동시 처리 제한
- [ ] 세마포어 또는 큐 시스템 구현
- [ ] 초과 요청 대기열 추가

### 상태 관리
- [ ] 대기 중인 요청 상태 반환
- [ ] 처리 중인 요청 카운트 모니터링

### 테스트
- [ ] 부하 테스트 작성

---

## 💻 구현 코드

### ReportGenerationLimiter.java

```java
package com.reacademix.reacademix_backend.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

@Slf4j
@Component
public class ReportGenerationLimiter {

    private static final int MAX_CONCURRENT_REPORTS = 10;
    private static final int WAIT_TIMEOUT_SECONDS = 60;

    private final Semaphore semaphore = new Semaphore(MAX_CONCURRENT_REPORTS);

    public boolean tryAcquire() {
        try {
            boolean acquired = semaphore.tryAcquire(WAIT_TIMEOUT_SECONDS, TimeUnit.SECONDS);
            if (acquired) {
                log.info("리포트 생성 슬롯 획득. 현재 사용 중: {}/{}", 
                    MAX_CONCURRENT_REPORTS - semaphore.availablePermits(), MAX_CONCURRENT_REPORTS);
            } else {
                log.warn("리포트 생성 슬롯 대기 시간 초과");
            }
            return acquired;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }

    public void release() {
        semaphore.release();
        log.info("리포트 생성 슬롯 반환. 현재 사용 중: {}/{}", 
            MAX_CONCURRENT_REPORTS - semaphore.availablePermits(), MAX_CONCURRENT_REPORTS);
    }

    public int getAvailableSlots() {
        return semaphore.availablePermits();
    }

    public int getQueueLength() {
        return semaphore.getQueueLength();
    }
}
```

### ReportService.java (동시 처리 적용)

```java
@Transactional
public GenerateReportResponseDto requestReportGeneration(
        GenerateReportRequestDto request, User currentUser) {

    // 동시 처리 제한 확인
    if (!reportGenerationLimiter.tryAcquire()) {
        throw new BusinessException(ErrorCode.BUSINESS_005, 
            "리포트 생성 대기열이 가득 찼습니다. 잠시 후 다시 시도해주세요.");
    }

    try {
        // ... 기존 로직
        
        // 비동기 생성 시작
        generateReportAsync(report.getId());
        
        return GenerateReportResponseDto.generating(report.getId());
        
    } catch (Exception e) {
        reportGenerationLimiter.release();
        throw e;
    }
}

@Async("reportGenerationExecutor")
@Transactional
public void generateReportAsync(Long reportId) {
    try {
        // ... 리포트 생성 로직
    } finally {
        reportGenerationLimiter.release();
    }
}
```

### ReportStatusController.java

```java
@GetMapping("/status/slots")
@Operation(summary = "리포트 생성 슬롯 현황", description = "현재 리포트 생성 가능 슬롯 수를 조회합니다.")
public ResponseEntity<ApiResponse<Map<String, Integer>>> getSlotStatus() {
    Map<String, Integer> status = Map.of(
        "availableSlots", reportGenerationLimiter.getAvailableSlots(),
        "waitingCount", reportGenerationLimiter.getQueueLength(),
        "maxSlots", 10
    );
    return ResponseEntity.ok(ApiResponse.success(status));
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-25
- **End**: 2025-12-29
- **Lane**: NFR

## 🔗 Traceability

- Related SRS: REQ-NF-004
- Related Epic: Performance
