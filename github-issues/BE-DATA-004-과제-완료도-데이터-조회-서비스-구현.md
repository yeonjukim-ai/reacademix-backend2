# 과제 완료도 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-004
- **REQ / Epic**: REQ-FUNC-006
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 과제 완료도 데이터를 조회하는 서비스를 구현합니다. 리포트 생성 시 과제 현황 섹션에 사용됩니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `AssignmentService` 클래스 생성
- [ ] `getAssignmentData(studentId, startDate, endDate)` 메서드 구현

### 비즈니스 로직
- [ ] 완료율 계산: (완료 과제 / 전체 과제) × 100
- [ ] 상태별 집계 (완료, 진행중, 미시작)
- [ ] 미완료 과제 목록 반환

### 성능 및 테스트
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### AssignmentDataDto.java

```java
package com.reacademix.reacademix_backend.dto.data;

import lombok.*;
import java.time.LocalDate;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AssignmentDataDto {
    private int totalCount;
    private int completedCount;
    private int inProgressCount;
    private int notStartedCount;
    private double completionRate;
    private List<AssignmentItem> incompleteAssignments;

    @Getter
    @Builder
    public static class AssignmentItem {
        private Long id;
        private String name;
        private String subject;
        private String status;
        private LocalDate dueDate;
        private boolean overdue;
    }
}
```

### AssignmentService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.assignment.Assignment;
import com.reacademix.reacademix_backend.domain.assignment.AssignmentStatus;
import com.reacademix.reacademix_backend.dto.data.AssignmentDataDto;
import com.reacademix.reacademix_backend.repository.AssignmentRepository;
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
@Transactional(readOnly = true)
public class AssignmentService {

    private final AssignmentRepository assignmentRepository;
    private static final int MAX_INCOMPLETE_ASSIGNMENTS = 10;

    public AssignmentDataDto getAssignmentData(Long studentId, LocalDate startDate, LocalDate endDate) {
        log.debug("과제 데이터 조회: studentId={}, period={} ~ {}", studentId, startDate, endDate);

        List<Assignment> assignments = assignmentRepository
            .findByStudentIdAndDueDateBetween(studentId, startDate, endDate);

        if (assignments.isEmpty()) {
            return AssignmentDataDto.builder()
                .totalCount(0)
                .completedCount(0)
                .inProgressCount(0)
                .notStartedCount(0)
                .completionRate(0.0)
                .incompleteAssignments(List.of())
                .build();
        }

        // 상태별 집계
        Map<AssignmentStatus, Long> statusCount = assignments.stream()
            .collect(Collectors.groupingBy(Assignment::getStatus, Collectors.counting()));

        int total = assignments.size();
        int completed = statusCount.getOrDefault(AssignmentStatus.COMPLETED, 0L).intValue();
        int inProgress = statusCount.getOrDefault(AssignmentStatus.IN_PROGRESS, 0L).intValue();
        int notStarted = statusCount.getOrDefault(AssignmentStatus.NOT_STARTED, 0L).intValue();

        double completionRate = total > 0 ? (completed * 100.0) / total : 0;

        // 미완료 과제 목록
        LocalDate today = LocalDate.now();
        List<AssignmentDataDto.AssignmentItem> incompleteList = assignments.stream()
            .filter(a -> a.getStatus() != AssignmentStatus.COMPLETED)
            .sorted((a, b) -> a.getDueDate().compareTo(b.getDueDate()))
            .limit(MAX_INCOMPLETE_ASSIGNMENTS)
            .map(a -> AssignmentDataDto.AssignmentItem.builder()
                .id(a.getId())
                .name(a.getName())
                .subject(a.getSubject())
                .status(a.getStatus().name())
                .dueDate(a.getDueDate())
                .overdue(a.getDueDate().isBefore(today))
                .build())
            .collect(Collectors.toList());

        return AssignmentDataDto.builder()
            .totalCount(total)
            .completedCount(completed)
            .inProgressCount(inProgress)
            .notStartedCount(notStarted)
            .completionRate(Math.round(completionRate * 10) / 10.0)
            .incompleteAssignments(incompleteList)
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

- Related SRS: REQ-FUNC-006
- Related Epic: Report Generation
