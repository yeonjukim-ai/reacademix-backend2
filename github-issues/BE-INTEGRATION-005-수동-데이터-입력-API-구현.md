# 수동 데이터 입력 API 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-005
- **REQ / Epic**: REQ-FUNC-016
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-INTEGRATION-002, BE-INTEGRATION-004

## 📌 Description

사용자가 수동으로 데이터를 입력할 수 있는 API를 구현합니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `POST /api/v1/data/manual` 엔드포인트 구현
- [ ] Request/Response DTO 생성
- [ ] 데이터 검증 후 저장

### 에러 처리
- [ ] 검증 실패 시 오류 반환
- [ ] 필수 필드 누락 시 400

### 테스트
- [ ] 단위 테스트 작성

---

## 📋 API 명세서

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `POST` |
| **URI** | `/api/v1/data/manual` |
| **Content-Type** | `application/json` |
| **인증 필요** | ✅ |

### Request Body

```json
{
  "dataType": "ATTENDANCE",
  "data": {
    "studentCode": "STU-001",
    "date": "2025-01-15",
    "status": "PRESENT"
  }
}
```

### Response Body (200 OK)

```json
{
  "success": true,
  "data": {
    "status": "SAVED",
    "message": "데이터가 저장되었습니다."
  }
}
```

---

## 💻 구현 코드

### ManualDataInputRequestDto.java

```java
@Getter
@Builder
public class ManualDataInputRequestDto {
    @NotBlank(message = "데이터 타입은 필수입니다.")
    private String dataType;

    @NotNull(message = "데이터는 필수입니다.")
    private Map<String, String> data;
}
```

### DataController.java

```java
@PostMapping("/manual")
@Operation(summary = "수동 데이터 입력", description = "단건 데이터를 수동으로 입력합니다.")
public ResponseEntity<ApiResponse<ManualInputResponseDto>> manualInput(
        @Valid @RequestBody ManualDataInputRequestDto request) {

    log.info("수동 데이터 입력: type={}", request.getDataType());

    // 검증
    ValidationResult validation = validationService.validateSingleData(
        request.getData(), request.getDataType());

    if (!validation.isValid()) {
        throw new BusinessException(ErrorCode.VALIDATION_001, 
            validation.getErrors().get(0).getMessage());
    }

    // 저장
    integrationService.integrateData(List.of(request.getData()), request.getDataType());

    return ResponseEntity.ok(ApiResponse.success(
        ManualInputResponseDto.builder()
            .status("SAVED")
            .message("데이터가 저장되었습니다.")
            .build()));
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-13
- **End**: 2025-12-15
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-016
- Related Epic: Data Integration
