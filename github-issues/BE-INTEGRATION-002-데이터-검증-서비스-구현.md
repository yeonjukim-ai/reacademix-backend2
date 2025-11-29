# 데이터 검증 서비스 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-002
- **REQ / Epic**: REQ-FUNC-018
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INTEGRATION-001

## 📌 Description

업로드된 데이터의 형식 및 범위를 검증하는 서비스를 구현합니다. 출석, 학습시간, 성적 등 데이터 타입별 검증 규칙을 적용합니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `DataValidationService` 클래스 생성
- [ ] `validateData(data, dataType)` 메서드 구현

### 검증 규칙
- [ ] 필수 필드 존재 여부 확인
- [ ] 데이터 타입 검증
- [ ] 값 범위 검증
- [ ] 날짜 형식 검증

### 검증 결과
- [ ] 검증 성공/실패 반환
- [ ] 실패 시 상세 오류 메시지

### 테스트
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### ValidationResult.java

```java
package com.reacademix.reacademix_backend.dto.validation;

import lombok.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ValidationResult {
    private boolean valid;
    private int totalRows;
    private int validRows;
    private int invalidRows;
    @Builder.Default
    private List<ValidationError> errors = new ArrayList<>();

    @Getter
    @Builder
    public static class ValidationError {
        private int rowNumber;
        private String field;
        private String value;
        private String message;
    }

    public void addError(int row, String field, String value, String message) {
        this.errors.add(ValidationError.builder()
            .rowNumber(row)
            .field(field)
            .value(value)
            .message(message)
            .build());
    }
}
```

### DataValidationService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.dto.validation.ValidationResult;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Slf4j
@Service
public class DataValidationService {

    // 데이터 타입별 필수 필드
    private static final Map<String, Set<String>> REQUIRED_FIELDS = Map.of(
        "ATTENDANCE", Set.of("studentCode", "date", "status"),
        "STUDY_TIME", Set.of("studentCode", "date", "subject", "minutes"),
        "MOCK_EXAM", Set.of("studentCode", "examDate", "subject", "score"),
        "ASSIGNMENT", Set.of("studentCode", "name", "dueDate", "status")
    );

    public ValidationResult validateData(List<Map<String, String>> data, String dataType) {
        log.info("데이터 검증 시작: type={}, rows={}", dataType, data.size());

        ValidationResult.ValidationResultBuilder result = ValidationResult.builder()
            .totalRows(data.size())
            .validRows(0)
            .invalidRows(0);

        Set<String> requiredFields = REQUIRED_FIELDS.getOrDefault(dataType, Set.of());
        int validCount = 0;
        int invalidCount = 0;
        List<ValidationResult.ValidationError> errors = new java.util.ArrayList<>();

        for (int i = 0; i < data.size(); i++) {
            Map<String, String> row = data.get(i);
            int rowNum = i + 2; // 헤더 제외, 1-based
            boolean rowValid = true;

            // 1. 필수 필드 검증
            for (String field : requiredFields) {
                if (!row.containsKey(field) || row.get(field).isBlank()) {
                    errors.add(ValidationResult.ValidationError.builder()
                        .rowNumber(rowNum)
                        .field(field)
                        .value("")
                        .message("필수 필드가 누락되었습니다.")
                        .build());
                    rowValid = false;
                }
            }

            // 2. 데이터 타입별 검증
            if (rowValid) {
                List<ValidationResult.ValidationError> typeErrors = 
                    validateByType(row, dataType, rowNum);
                if (!typeErrors.isEmpty()) {
                    errors.addAll(typeErrors);
                    rowValid = false;
                }
            }

            if (rowValid) validCount++;
            else invalidCount++;
        }

        boolean isValid = invalidCount == 0;
        log.info("데이터 검증 완료: valid={}, validRows={}, invalidRows={}", 
            isValid, validCount, invalidCount);

        return result
            .valid(isValid)
            .validRows(validCount)
            .invalidRows(invalidCount)
            .errors(errors)
            .build();
    }

    private List<ValidationResult.ValidationError> validateByType(
            Map<String, String> row, String dataType, int rowNum) {
        List<ValidationResult.ValidationError> errors = new java.util.ArrayList<>();

        switch (dataType) {
            case "ATTENDANCE" -> validateAttendance(row, rowNum, errors);
            case "STUDY_TIME" -> validateStudyTime(row, rowNum, errors);
            case "MOCK_EXAM" -> validateMockExam(row, rowNum, errors);
            case "ASSIGNMENT" -> validateAssignment(row, rowNum, errors);
        }

        return errors;
    }

    private void validateAttendance(Map<String, String> row, int rowNum, 
                                    List<ValidationResult.ValidationError> errors) {
        // 날짜 형식 검증
        if (!isValidDate(row.get("date"))) {
            errors.add(createError(rowNum, "date", row.get("date"), 
                "유효한 날짜 형식이 아닙니다. (YYYY-MM-DD)"));
        }

        // 상태 값 검증
        String status = row.get("status");
        if (!Set.of("PRESENT", "ABSENT", "LATE", "EARLY_LEAVE").contains(status)) {
            errors.add(createError(rowNum, "status", status, 
                "유효한 출석 상태가 아닙니다. (PRESENT, ABSENT, LATE, EARLY_LEAVE)"));
        }
    }

    private void validateStudyTime(Map<String, String> row, int rowNum,
                                   List<ValidationResult.ValidationError> errors) {
        // 날짜 검증
        if (!isValidDate(row.get("date"))) {
            errors.add(createError(rowNum, "date", row.get("date"), 
                "유효한 날짜 형식이 아닙니다."));
        }

        // 시간(분) 검증
        String minutes = row.get("minutes");
        if (!isValidPositiveInteger(minutes) || Integer.parseInt(minutes) > 1440) {
            errors.add(createError(rowNum, "minutes", minutes, 
                "학습 시간은 0~1440 사이의 숫자여야 합니다."));
        }
    }

    private void validateMockExam(Map<String, String> row, int rowNum,
                                  List<ValidationResult.ValidationError> errors) {
        // 점수 검증
        String score = row.get("score");
        if (!isValidPositiveInteger(score) || Integer.parseInt(score) > 200) {
            errors.add(createError(rowNum, "score", score, 
                "점수는 0~200 사이의 숫자여야 합니다."));
        }
    }

    private void validateAssignment(Map<String, String> row, int rowNum,
                                    List<ValidationResult.ValidationError> errors) {
        // 상태 검증
        String status = row.get("status");
        if (!Set.of("COMPLETED", "IN_PROGRESS", "NOT_STARTED").contains(status)) {
            errors.add(createError(rowNum, "status", status, 
                "유효한 과제 상태가 아닙니다."));
        }
    }

    private boolean isValidDate(String value) {
        try {
            LocalDate.parse(value);
            return true;
        } catch (DateTimeParseException e) {
            return false;
        }
    }

    private boolean isValidPositiveInteger(String value) {
        try {
            return Integer.parseInt(value) >= 0;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    private ValidationResult.ValidationError createError(
            int rowNum, String field, String value, String message) {
        return ValidationResult.ValidationError.builder()
            .rowNumber(rowNum)
            .field(field)
            .value(value)
            .message(message)
            .build();
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-11-30
- **End**: 2025-12-03
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-018
- Related Epic: Data Integration
