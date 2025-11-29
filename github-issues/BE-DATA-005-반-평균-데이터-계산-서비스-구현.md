# 반 평균 데이터 계산 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-005
- **REQ / Epic**: REQ-FUNC-007
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생이 속한 반의 평균 데이터를 계산하는 서비스를 구현합니다. MVP에서는 간소화된 계산 로직을 사용합니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `ClassAverageService` 클래스 생성
- [ ] `getClassAverageData(classId, startDate, endDate)` 메서드 구현

### 비즈니스 로직
- [ ] 반 평균 출석률 계산
- [ ] 반 평균 학습 시간 계산
- [ ] 반 평균 모의고사 성적 계산
- [ ] 학생과 반 평균 비교

### 성능 및 테스트
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### ClassAverageDataDto.java

```java
package com.reacademix.reacademix_backend.dto.data;

import lombok.*;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ClassAverageDataDto {
    private double avgAttendanceRate;
    private double avgStudyTimeMinutes;
    private double avgMockExamScore;
    private double avgAssignmentCompletionRate;

    // 학생과의 비교 결과
    private ComparisonResult comparison;

    @Getter
    @Builder
    public static class ComparisonResult {
        private double attendanceDiff;     // 학생 - 반평균
        private double studyTimeDiff;
        private double mockExamDiff;
        private double assignmentDiff;
        
        private String attendanceStatus;   // ABOVE, BELOW, SAME
        private String studyTimeStatus;
        private String mockExamStatus;
        private String assignmentStatus;
    }
}
```

### ClassAverageService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.dto.data.ClassAverageDataDto;
import com.reacademix.reacademix_backend.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class ClassAverageService {

    private final AttendanceRepository attendanceRepository;
    private final StudyTimeRepository studyTimeRepository;
    private final MockExamRepository mockExamRepository;
    private final AssignmentRepository assignmentRepository;

    public ClassAverageDataDto getClassAverageData(Long classId, LocalDate startDate, LocalDate endDate) {
        log.debug("반 평균 데이터 조회: classId={}, period={} ~ {}", classId, startDate, endDate);

        // 반 평균 계산 (실제 쿼리로 계산)
        Double avgAttendance = attendanceRepository
            .calculateAverageAttendanceRateByClass(classId, startDate, endDate);
        
        Double avgStudyTime = studyTimeRepository
            .calculateAverageStudyTimeByClass(classId, startDate, endDate);
        
        Double avgMockExam = mockExamRepository
            .calculateAverageScoreByClass(classId, startDate, endDate);
        
        Double avgAssignment = assignmentRepository
            .calculateAverageCompletionRateByClass(classId, startDate, endDate);

        return ClassAverageDataDto.builder()
            .avgAttendanceRate(avgAttendance != null ? avgAttendance : 0.0)
            .avgStudyTimeMinutes(avgStudyTime != null ? avgStudyTime : 0.0)
            .avgMockExamScore(avgMockExam != null ? avgMockExam : 0.0)
            .avgAssignmentCompletionRate(avgAssignment != null ? avgAssignment : 0.0)
            .build();
    }

    /**
     * 학생과 반 평균 비교
     */
    public ClassAverageDataDto.ComparisonResult compareWithStudent(
            ClassAverageDataDto classAvg,
            double studentAttendance,
            double studentStudyTime,
            double studentMockExam,
            double studentAssignment) {

        return ClassAverageDataDto.ComparisonResult.builder()
            .attendanceDiff(studentAttendance - classAvg.getAvgAttendanceRate())
            .studyTimeDiff(studentStudyTime - classAvg.getAvgStudyTimeMinutes())
            .mockExamDiff(studentMockExam - classAvg.getAvgMockExamScore())
            .assignmentDiff(studentAssignment - classAvg.getAvgAssignmentCompletionRate())
            .attendanceStatus(getComparisonStatus(studentAttendance, classAvg.getAvgAttendanceRate()))
            .studyTimeStatus(getComparisonStatus(studentStudyTime, classAvg.getAvgStudyTimeMinutes()))
            .mockExamStatus(getComparisonStatus(studentMockExam, classAvg.getAvgMockExamScore()))
            .assignmentStatus(getComparisonStatus(studentAssignment, classAvg.getAvgAssignmentCompletionRate()))
            .build();
    }

    private String getComparisonStatus(double studentValue, double avgValue) {
        double threshold = 5.0; // 5% 이상 차이나면 ABOVE/BELOW
        if (studentValue > avgValue + threshold) return "ABOVE";
        if (studentValue < avgValue - threshold) return "BELOW";
        return "SAME";
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-10
- **Lane**: Financial

## 🔗 Traceability

- Related SRS: REQ-FUNC-007
- Related Epic: Report Generation
