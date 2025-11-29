# 통합 대시보드 조회 API 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-007
- **REQ / Epic**: REQ-FUNC-021
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-AUTH-002, BE-INTEGRATION-006

## 📌 Description

통합 대시보드 데이터를 조회하는 API를 구현합니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `GET /api/v1/dashboard` 엔드포인트 구현
- [ ] 기간 필터 (daily, weekly, monthly)
- [ ] 반 필터

### 성능 및 테스트
- [ ] 응답 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 📋 API 명세서

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **URI** | `/api/v1/dashboard` |
| **인증 필요** | ✅ |

### Query Parameters

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| period | String | ❌ | 기간 (daily, weekly, monthly). 기본: weekly |
| classId | Long | ❌ | 반 ID 필터 |

### Response Body

```json
{
  "success": true,
  "data": {
    "attendance": {
      "averageRate": 92.5,
      "totalStudents": 30,
      "presentToday": 28,
      "absentToday": 2
    },
    "studyTime": {
      "averageMinutesPerDay": 360,
      "totalHours": 1260,
      "completionRate": 85.5,
      "bySubject": [
        {"subject": "국어", "minutes": 300},
        {"subject": "수학", "minutes": 400}
      ]
    },
    "mockExam": {
      "averageScore": 78.5,
      "examCount": 3,
      "trend": "UP"
    },
    "assignment": {
      "completionRate": 82.0,
      "totalAssignments": 50,
      "completedCount": 41,
      "overdueCount": 3
    },
    "alerts": [
      {
        "type": "WARNING",
        "message": "마감 기한이 지난 과제가 3건 있습니다."
      }
    ]
  }
}
```

---

## 💻 구현 코드

### DashboardController.java

```java
@Tag(name = "Dashboard", description = "대시보드 API")
@RestController
@RequestMapping("/api/v1/dashboard")
@RequiredArgsConstructor
@Slf4j
public class DashboardController {

    private final DashboardService dashboardService;

    @GetMapping
    @Operation(summary = "대시보드 조회", description = "통합 대시보드 데이터를 조회합니다.")
    public ResponseEntity<ApiResponse<DashboardDataDto>> getDashboard(
            @RequestParam(defaultValue = "weekly") String period,
            @RequestParam(required = false) Long classId) {

        log.info("대시보드 조회: period={}, classId={}", period, classId);

        // period 값 검증
        if (!List.of("daily", "weekly", "monthly").contains(period)) {
            throw new BusinessException(ErrorCode.VALIDATION_001, 
                "유효하지 않은 기간입니다. (daily, weekly, monthly)");
        }

        DashboardDataDto dashboard = dashboardService.getDashboardData(period, classId);

        return ResponseEntity.ok(ApiResponse.success(dashboard));
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-021
- Related Epic: Data Integration
