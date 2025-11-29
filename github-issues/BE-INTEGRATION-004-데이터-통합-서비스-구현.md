# 데이터 통합 서비스 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-004
- **REQ / Epic**: REQ-FUNC-019
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INTEGRATION-002, BE-INFRA-003

## 📌 Description

여러 시스템에서 수집된 데이터를 학생 ID 기준으로 통합하여 데이터베이스에 저장하는 서비스를 구현합니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `DataIntegrationService` 클래스 생성
- [ ] `integrateData(data, dataType)` 메서드 구현
- [ ] 학생 ID 기준 데이터 그룹핑

### 저장 로직
- [ ] Batch Insert 사용 (JPA)
- [ ] 중복 데이터 처리 (Update or Skip)
- [ ] 데이터 타입별 테이블 저장

### 성능 및 테스트
- [ ] 처리 시간 2분 이내 (학원당)
- [ ] 데이터 통합 정확도 99% 이상
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### DataIntegrationService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.attendance.Attendance;
import com.reacademix.reacademix_backend.domain.student.Student;
import com.reacademix.reacademix_backend.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class DataIntegrationService {

    private final StudentRepository studentRepository;
    private final AttendanceRepository attendanceRepository;
    private final StudyTimeRepository studyTimeRepository;
    private final MockExamRepository mockExamRepository;
    private final AssignmentRepository assignmentRepository;

    @Transactional
    public IntegrationResult integrateData(List<Map<String, String>> data, String dataType) {
        log.info("데이터 통합 시작: type={}, rows={}", dataType, data.size());

        int savedCount = 0;
        int skippedCount = 0;
        int errorCount = 0;

        // 학생 코드로 그룹핑
        Map<String, List<Map<String, String>>> groupedByStudent = data.stream()
            .collect(Collectors.groupingBy(row -> row.get("studentCode")));

        for (Map.Entry<String, List<Map<String, String>>> entry : groupedByStudent.entrySet()) {
            String studentCode = entry.getKey();
            List<Map<String, String>> studentData = entry.getValue();

            Student student = studentRepository.findByStudentCode(studentCode).orElse(null);
            if (student == null) {
                log.warn("학생을 찾을 수 없음: studentCode={}", studentCode);
                skippedCount += studentData.size();
                continue;
            }

            try {
                int saved = saveDataByType(student, studentData, dataType);
                savedCount += saved;
            } catch (Exception e) {
                log.error("데이터 저장 실패: studentCode={}, error={}", studentCode, e.getMessage());
                errorCount += studentData.size();
            }
        }

        log.info("데이터 통합 완료: saved={}, skipped={}, errors={}", 
            savedCount, skippedCount, errorCount);

        return IntegrationResult.builder()
            .totalRows(data.size())
            .savedRows(savedCount)
            .skippedRows(skippedCount)
            .errorRows(errorCount)
            .build();
    }

    private int saveDataByType(Student student, List<Map<String, String>> data, String dataType) {
        return switch (dataType) {
            case "ATTENDANCE" -> saveAttendanceData(student, data);
            case "STUDY_TIME" -> saveStudyTimeData(student, data);
            case "MOCK_EXAM" -> saveMockExamData(student, data);
            case "ASSIGNMENT" -> saveAssignmentData(student, data);
            default -> throw new IllegalArgumentException("Unknown data type: " + dataType);
        };
    }

    private int saveAttendanceData(Student student, List<Map<String, String>> data) {
        List<Attendance> attendances = data.stream()
            .map(row -> Attendance.builder()
                .student(student)
                .attendanceDate(LocalDate.parse(row.get("date")))
                .status(AttendanceStatus.valueOf(row.get("status")))
                .build())
            .collect(Collectors.toList());

        attendanceRepository.saveAll(attendances);
        return attendances.size();
    }

    // 다른 데이터 타입도 유사하게 구현...

    @lombok.Getter
    @lombok.Builder
    public static class IntegrationResult {
        private int totalRows;
        private int savedRows;
        private int skippedRows;
        private int errorRows;
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-12
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-019
- Related Epic: Data Integration
