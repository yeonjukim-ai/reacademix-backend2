# 학습 시간 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-002
- **REQ / Epic**: REQ-FUNC-004
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 학습 시간 데이터를 조회하고 집계하는 서비스를 구현합니다. 리포트 생성 시 학습 시간 섹션에 사용됩니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `StudyTimeService` 클래스 생성
- [ ] `getStudyTimeData(studentId, startDate, endDate)` 메서드 구현

### 비즈니스 로직
- [ ] 일평균 학습 시간 계산
- [ ] 주평균 학습 시간 계산
- [ ] 목표 대비 달성률 계산
- [ ] 과목별 학습 시간 집계

### 성능 및 테스트
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### StudyTimeDataDto.java

```java
package com.reacademix.reacademix_backend.dto.data;

import lombok.*;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudyTimeDataDto {
    private int totalPlannedMinutes;
    private int totalActualMinutes;
    private double dailyAverageMinutes;
    private double weeklyAverageMinutes;
    private double completionRate;
    private List<SubjectStudyTime> bySubject;
    private List<DailyStudyTime> dailyRecords;

    @Getter
    @Builder
    public static class SubjectStudyTime {
        private String subject;
        private int plannedMinutes;
        private int actualMinutes;
        private double completionRate;
    }

    @Getter
    @Builder
    public static class DailyStudyTime {
        private String date;
        private int plannedMinutes;
        private int actualMinutes;
    }
}
```

### StudyTimeService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.studytime.StudyTime;
import com.reacademix.reacademix_backend.dto.data.StudyTimeDataDto;
import com.reacademix.reacademix_backend.repository.StudyTimeRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StudyTimeService {

    private final StudyTimeRepository studyTimeRepository;

    public StudyTimeDataDto getStudyTimeData(Long studentId, LocalDate startDate, LocalDate endDate) {
        log.debug("학습 시간 데이터 조회: studentId={}, period={} ~ {}", studentId, startDate, endDate);

        List<StudyTime> records = studyTimeRepository
            .findByStudentIdAndStudyDateBetween(studentId, startDate, endDate);

        if (records.isEmpty()) {
            return StudyTimeDataDto.builder()
                .totalPlannedMinutes(0)
                .totalActualMinutes(0)
                .dailyAverageMinutes(0.0)
                .weeklyAverageMinutes(0.0)
                .completionRate(0.0)
                .bySubject(List.of())
                .dailyRecords(List.of())
                .build();
        }

        // 총합 계산
        int totalPlanned = records.stream().mapToInt(StudyTime::getPlannedMinutes).sum();
        int totalActual = records.stream().mapToInt(StudyTime::getActualMinutes).sum();

        // 기간 계산
        long days = ChronoUnit.DAYS.between(startDate, endDate) + 1;
        long weeks = Math.max(1, days / 7);

        // 평균 계산
        double dailyAverage = days > 0 ? (double) totalActual / days : 0;
        double weeklyAverage = weeks > 0 ? (double) totalActual / weeks : 0;
        double completionRate = totalPlanned > 0 ? (totalActual * 100.0) / totalPlanned : 0;

        // 과목별 집계
        Map<String, List<StudyTime>> bySubject = records.stream()
            .collect(Collectors.groupingBy(StudyTime::getSubject));

        List<StudyTimeDataDto.SubjectStudyTime> subjectData = bySubject.entrySet().stream()
            .map(e -> {
                int planned = e.getValue().stream().mapToInt(StudyTime::getPlannedMinutes).sum();
                int actual = e.getValue().stream().mapToInt(StudyTime::getActualMinutes).sum();
                return StudyTimeDataDto.SubjectStudyTime.builder()
                    .subject(e.getKey())
                    .plannedMinutes(planned)
                    .actualMinutes(actual)
                    .completionRate(planned > 0 ? (actual * 100.0) / planned : 0)
                    .build();
            })
            .collect(Collectors.toList());

        return StudyTimeDataDto.builder()
            .totalPlannedMinutes(totalPlanned)
            .totalActualMinutes(totalActual)
            .dailyAverageMinutes(Math.round(dailyAverage * 10) / 10.0)
            .weeklyAverageMinutes(Math.round(weeklyAverage * 10) / 10.0)
            .completionRate(Math.round(completionRate * 10) / 10.0)
            .bySubject(subjectData)
            .build();
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial

## 🔗 Traceability

- Related SRS: REQ-FUNC-004
- Related Epic: Report Generation
