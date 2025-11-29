# 리포트 전송 이력 조회 API 구현

- **Type**: Functional
- **Key**: BE-DELIVERY-002
- **REQ / Epic**: REQ-FUNC-028
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-DELIVERY-001

## 📌 Description

리포트 전송 이력을 조회하는 API를 구현합니다. 페이지네이션과 필터링을 지원합니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `GET /api/v1/reports/delivery/history` 엔드포인트 구현
- [ ] 학생별 필터링
- [ ] 페이지네이션

### 성능 및 테스트
- [ ] 응답 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 📋 API 명세서

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **URI** | `/api/v1/reports/delivery/history` |
| **인증 필요** | ✅ |

### Query Parameters

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| studentId | Long | ❌ | 학생 ID 필터 |
| page | int | ❌ | 페이지 번호 (기본: 0) |
| size | int | ❌ | 페이지 크기 (기본: 20) |

### Response Body

```json
{
  "success": true,
  "data": {
    "content": [
      {
        "deliveryId": 1,
        "reportId": 1,
        "studentName": "김철수",
        "recipientEmail": "parent@example.com",
        "status": "SUCCESS",
        "sentAt": "2025-01-15T10:30:00"
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

### DeliveryHistoryDto.java

```java
@Getter
@Builder
public class DeliveryHistoryDto {
    private Long deliveryId;
    private Long reportId;
    private String studentName;
    private String recipientEmail;
    private String status;
    private LocalDateTime sentAt;

    public static DeliveryHistoryDto from(ReportDelivery delivery) {
        return DeliveryHistoryDto.builder()
            .deliveryId(delivery.getId())
            .reportId(delivery.getReport().getId())
            .studentName(delivery.getReport().getStudent().getName())
            .recipientEmail(delivery.getRecipientEmail())
            .status(delivery.getStatus().name())
            .sentAt(delivery.getSentAt())
            .build();
    }
}
```

### ReportController.java

```java
@GetMapping("/delivery/history")
@Operation(summary = "전송 이력 조회", description = "리포트 전송 이력을 조회합니다.")
public ResponseEntity<ApiResponse<Page<DeliveryHistoryDto>>> getDeliveryHistory(
        @RequestParam(required = false) Long studentId,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size) {
    
    Page<DeliveryHistoryDto> history = reportDeliveryService.getDeliveryHistory(
        studentId, PageRequest.of(page, size, Sort.by("sentAt").descending()));
    
    return ResponseEntity.ok(ApiResponse.success(history));
}
```

### ReportDeliveryService.java

```java
@Transactional(readOnly = true)
public Page<DeliveryHistoryDto> getDeliveryHistory(Long studentId, Pageable pageable) {
    Page<ReportDelivery> deliveries;
    
    if (studentId != null) {
        deliveries = deliveryRepository.findByReportStudentId(studentId, pageable);
    } else {
        deliveries = deliveryRepository.findAll(pageable);
    }
    
    return deliveries.map(DeliveryHistoryDto::from);
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-028
- Related Epic: Report Delivery
