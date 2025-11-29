# 리포트 생성 이력 조회 API 구현

- **Type**: Functional
- **Key**: BE-REPORT-007
- **REQ / Epic**: REQ-FUNC-013
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-REPORT-005

## 📌 Description

리포트 생성 이력을 조회하는 API를 구현합니다. 페이지네이션과 필터링을 지원합니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `GET /api/v1/reports/history` 엔드포인트 구현
- [ ] 학생별, 상태별 필터링
- [ ] 페이지네이션

### 성능 및 테스트
- [ ] 응답 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 📋 API 명세서

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **URI** | `/api/v1/reports/history` |
| **인증 필요** | ✅ |

### Query Parameters

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| studentId | Long | ❌ | 학생 ID 필터 |
| status | String | ❌ | 상태 필터 (COMPLETED, FAILED) |
| page | int | ❌ | 페이지 번호 (기본: 0) |
| size | int | ❌ | 페이지 크기 (기본: 20) |

### Response Body

```json
{
  "success": true,
  "data": {
    "content": [
      {
        "reportId": 1,
        "studentId": 1,
        "studentName": "김철수",
        "reportStartDate": "2025-01-01",
        "reportEndDate": "2025-01-31",
        "status": "COMPLETED",
        "fileSize": 1024000,
        "generationDurationMs": 15230,
        "createdAt": "2025-01-15T10:30:00",
        "downloadCount": 3
      }
    ],
    "totalElements": 50,
    "totalPages": 3,
    "currentPage": 0
  }
}
```

---

## 💻 구현 코드

### ReportHistoryDto.java

```java
@Getter
@Builder
public class ReportHistoryDto {
    private Long reportId;
    private Long studentId;
    private String studentName;
    private LocalDate reportStartDate;
    private LocalDate reportEndDate;
    private String status;
    private Long fileSize;
    private Long generationDurationMs;
    private LocalDateTime createdAt;
    private int downloadCount;

    public static ReportHistoryDto from(Report report) {
        return ReportHistoryDto.builder()
            .reportId(report.getId())
            .studentId(report.getStudent().getId())
            .studentName(report.getStudent().getName())
            .reportStartDate(report.getReportStartDate())
            .reportEndDate(report.getReportEndDate())
            .status(report.getStatus().name())
            .fileSize(report.getFileSize())
            .generationDurationMs(report.getGenerationDurationMs())
            .createdAt(report.getCreatedAt())
            .downloadCount(report.getDownloadCount())
            .build();
    }
}
```

### ReportController.java

```java
@GetMapping("/history")
@Operation(summary = "리포트 이력 조회", description = "리포트 생성 이력을 조회합니다.")
public ResponseEntity<ApiResponse<Page<ReportHistoryDto>>> getReportHistory(
        @RequestParam(required = false) Long studentId,
        @RequestParam(required = false) String status,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size) {

    Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
    
    Page<ReportHistoryDto> history = reportService.getReportHistory(studentId, status, pageable);

    return ResponseEntity.ok(ApiResponse.success(history));
}
```

### ReportService.java

```java
@Transactional(readOnly = true)
public Page<ReportHistoryDto> getReportHistory(Long studentId, String status, Pageable pageable) {
    Page<Report> reports;

    if (studentId != null && status != null) {
        reports = reportRepository.findByStudentIdAndStatus(
            studentId, ReportStatus.valueOf(status), pageable);
    } else if (studentId != null) {
        reports = reportRepository.findByStudentId(studentId, pageable);
    } else if (status != null) {
        reports = reportRepository.findByStatus(ReportStatus.valueOf(status), pageable);
    } else {
        reports = reportRepository.findAll(pageable);
    }

    return reports.map(ReportHistoryDto::from);
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-27
- **End**: 2025-12-29
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-013
- Related Epic: Report Generation
