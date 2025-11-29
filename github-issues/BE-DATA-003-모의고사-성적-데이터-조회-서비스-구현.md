# 모의고사 성적 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-003
- **REQ / Epic**: REQ-FUNC-005
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 모의고사 성적 데이터를 조회하고 분석하는 서비스를 구현합니다. 리포트 생성 시 성적 섹션에 사용됩니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `MockExamService` 클래스 생성
- [ ] `getMockExamData(studentId, startDate, endDate)` 메서드 구현

### 비즈니스 로직
- [ ] 기간 내 모의고사 성적 조회
- [ ] 과목별 성적 집계
- [ ] 성적 추이 분석 (상승/하락/유지)
- [ ] 등급 변화 분석

### 성능 및 테스트
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### MockExamDataDto.java

```java
package com.reacademix.reacademix_backend.dto.data;

import lombok.*;
import java.time.LocalDate;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MockExamDataDto {
    private List<ExamResult> results;
    private String trend;  // IMPROVING, DECLINING, STABLE
    private String gradeChange;  // UP, DOWN, SAME

    @Getter
    @Builder
    public static class ExamResult {
        private LocalDate examDate;
        private String examName;
        private String subject;
        private int score;
        private int maxScore;
        private Integer rank;
        private Integer totalStudents;
        private double scoreRate;
    }
}
```

### MockExamService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.mockexam.MockExam;
import com.reacademix.reacademix_backend.dto.data.MockExamDataDto;
import com.reacademix.reacademix_backend.repository.MockExamRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MockExamService {

    private final MockExamRepository mockExamRepository;

    public MockExamDataDto getMockExamData(Long studentId, LocalDate startDate, LocalDate endDate) {
        log.debug("모의고사 데이터 조회: studentId={}, period={} ~ {}", studentId, startDate, endDate);

        List<MockExam> exams = mockExamRepository
            .findByStudentIdAndExamDateBetween(studentId, startDate, endDate);

        if (exams.isEmpty()) {
            return MockExamDataDto.builder()
                .results(List.of())
                .trend("STABLE")
                .gradeChange("SAME")
                .build();
        }

        // 결과 변환
        List<MockExamDataDto.ExamResult> results = exams.stream()
            .sorted(Comparator.comparing(MockExam::getExamDate).reversed())
            .map(e -> MockExamDataDto.ExamResult.builder()
                .examDate(e.getExamDate())
                .examName(e.getExamName())
                .subject(e.getSubject())
                .score(e.getScore())
                .maxScore(e.getMaxScore())
                .rank(e.getRank())
                .totalStudents(e.getTotalStudents())
                .scoreRate(e.getMaxScore() > 0 ? (e.getScore() * 100.0) / e.getMaxScore() : 0)
                .build())
            .collect(Collectors.toList());

        // 추이 분석
        String trend = analyzeTrend(exams);
        String gradeChange = analyzeGradeChange(exams);

        return MockExamDataDto.builder()
            .results(results)
            .trend(trend)
            .gradeChange(gradeChange)
            .build();
    }

    private String analyzeTrend(List<MockExam> exams) {
        if (exams.size() < 2) return "STABLE";

        List<MockExam> sorted = exams.stream()
            .sorted(Comparator.comparing(MockExam::getExamDate))
            .toList();

        int firstHalfAvg = sorted.subList(0, sorted.size() / 2).stream()
            .mapToInt(MockExam::getScore).sum() / (sorted.size() / 2);
        int secondHalfAvg = sorted.subList(sorted.size() / 2, sorted.size()).stream()
            .mapToInt(MockExam::getScore).sum() / (sorted.size() - sorted.size() / 2);

        if (secondHalfAvg > firstHalfAvg + 5) return "IMPROVING";
        if (secondHalfAvg < firstHalfAvg - 5) return "DECLINING";
        return "STABLE";
    }

    private String analyzeGradeChange(List<MockExam> exams) {
        if (exams.size() < 2) return "SAME";

        List<MockExam> sorted = exams.stream()
            .sorted(Comparator.comparing(MockExam::getExamDate))
            .filter(e -> e.getRank() != null)
            .toList();

        if (sorted.size() < 2) return "SAME";

        Integer firstRank = sorted.get(0).getRank();
        Integer lastRank = sorted.get(sorted.size() - 1).getRank();

        if (lastRank < firstRank) return "UP";  // 등급은 숫자가 작을수록 좋음
        if (lastRank > firstRank) return "DOWN";
        return "SAME";
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial

## 🔗 Traceability

- Related SRS: REQ-FUNC-005
- Related Epic: Report Generation
