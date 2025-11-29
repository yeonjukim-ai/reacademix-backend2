# 리포트 생성 시간 제한 및 모니터링 구현

- **Type**: Functional
- **Key**: BE-REPORT-004
- **REQ / Epic**: REQ-FUNC-011
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-REPORT-003

## 📌 Description

리포트 생성 시간을 모니터링하고, 30초를 초과하면 실패 처리하는 로직을 구현합니다.

## ✅ Acceptance Criteria

### 시간 제한 구현
- [ ] 생성 시작 시간 기록
- [ ] 30초 타임아웃 설정
- [ ] 타임아웃 시 자동 취소

### 모니터링
- [ ] 단계별 소요 시간 로깅
- [ ] 느린 생성 경고 알림

### 테스트
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### ReportGenerationConfig.java

```java
@Configuration
public class ReportGenerationConfig {
    
    public static final int TIMEOUT_SECONDS = 30;
    
    @Bean
    public ExecutorService reportGenerationExecutor() {
        return Executors.newFixedThreadPool(10);
    }
}
```

### ReportService.java (시간 제한 적용)

```java
@Transactional
public Report generateReportWithTimeout(Long studentId, LocalDate startDate, LocalDate endDate, User createdBy) {
    log.info("리포트 생성 시작 (timeout: {}s)", ReportGenerationConfig.TIMEOUT_SECONDS);
    
    // Report 엔티티 생성
    Report report = createInitialReport(studentId, startDate, endDate, createdBy);
    
    ExecutorService executor = reportGenerationExecutor;
    Future<Report> future = executor.submit(() -> {
        return executeReportGeneration(report, studentId, startDate, endDate);
    });
    
    try {
        return future.get(ReportGenerationConfig.TIMEOUT_SECONDS, TimeUnit.SECONDS);
        
    } catch (TimeoutException e) {
        log.error("리포트 생성 타임아웃: reportId={}", report.getId());
        future.cancel(true);
        
        report.markAsFailed("생성 시간이 30초를 초과했습니다.");
        reportRepository.save(report);
        
        throw new BusinessException(ErrorCode.TIMEOUT_001, "리포트 생성 시간이 초과되었습니다. (30초)");
        
    } catch (Exception e) {
        log.error("리포트 생성 실패: {}", e.getMessage());
        report.markAsFailed(e.getMessage());
        reportRepository.save(report);
        throw new BusinessException(ErrorCode.BUSINESS_001, "리포트 생성에 실패했습니다.");
    }
}

private Report executeReportGeneration(Report report, Long studentId, LocalDate startDate, LocalDate endDate) {
    StopWatch stopWatch = new StopWatch("ReportGeneration");
    
    // 1. 데이터 수집
    stopWatch.start("DataCollection");
    ReportDataDto reportData = collectReportData(studentId, startDate, endDate);
    stopWatch.stop();
    log.info("데이터 수집 완료: {}ms", stopWatch.getLastTaskTimeMillis());
    
    // 2. 인사이트 생성
    stopWatch.start("InsightGeneration");
    List<String> insights = insightService.generateInsights(reportData);
    stopWatch.stop();
    log.info("인사이트 생성 완료: {}ms", stopWatch.getLastTaskTimeMillis());
    
    // 3. HTML 렌더링
    stopWatch.start("HtmlRendering");
    String html = templateService.renderTemplate(reportData.toBuilder().insights(insights).build());
    stopWatch.stop();
    log.info("HTML 렌더링 완료: {}ms", stopWatch.getLastTaskTimeMillis());
    
    // 4. PDF 생성
    stopWatch.start("PdfGeneration");
    ReportPdfService.PdfGenerationResult pdfResult = pdfService.generatePdf(html, studentCode);
    stopWatch.stop();
    log.info("PDF 생성 완료: {}ms", stopWatch.getLastTaskTimeMillis());
    
    // 총 소요 시간 로깅
    log.info("리포트 생성 완료 - 총 소요 시간: {}ms", stopWatch.getTotalTimeMillis());
    
    // 경고 (20초 이상)
    if (stopWatch.getTotalTimeMillis() > 20000) {
        log.warn("리포트 생성 시간 경고: {}ms (임계값: 20000ms)", stopWatch.getTotalTimeMillis());
    }
    
    report.markAsCompleted(pdfResult.getFilePath(), pdfResult.getFileSize(), toJson(insights));
    return reportRepository.save(report);
}
```

### ErrorCode.java (추가)

```java
// 타임아웃 에러 코드
TIMEOUT_001("TIMEOUT_001", "작업 시간이 초과되었습니다.", HttpStatus.REQUEST_TIMEOUT)
```

---

## 📊 모니터링 지표

| 단계 | 목표 시간 | 경고 임계값 |
|------|----------|------------|
| 데이터 수집 | ≤ 5초 | > 8초 |
| 인사이트 생성 | ≤ 1초 | > 2초 |
| HTML 렌더링 | ≤ 1초 | > 2초 |
| PDF 생성 | ≤ 20초 | > 25초 |
| **총 시간** | **≤ 30초** | **> 25초** |

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-25
- **End**: 2025-12-27
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-011
- Related Epic: Report Generation
