# 통합 대시보드 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-006
- **REQ / Epic**: REQ-FUNC-021
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

통합된 데이터를 대시보드 형태로 조회하는 서비스를 구현합니다. 출석률, 학습 시간, 모의고사 성적을 집계합니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `DashboardService` 클래스 생성
- [ ] `getDashboardData(period, classId)` 메서드 구현

### 데이터 집계
- [ ] 기간별 출석률 집계
- [ ] 기간별 학습 시간 집계
- [ ] 기간별 모의고사 평균 집계
- [ ] 과제 완료율 집계

### 성능 및 테스트
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### DashboardDataDto.java

```java
package com.reacademix.reacademix_backend.dto.dashboard;

import lombok.*;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DashboardDataDto {
    private AttendanceSummary attendance;
    private StudyTimeSummary studyTime;
    private MockExamSummary mockExam;
    private AssignmentSummary assignment;
    private List<TopStudentDto> topStudents;
    private List<AlertDto> alerts;

    @Getter
    @Builder
    public static class AttendanceSummary {
        private double averageRate;
        private int totalStudents;
        private int presentToday;
        private int absentToday;
        private List<DailyRate> trend;
    }

    @Getter
    @Builder
    public static class StudyTimeSummary {
        private double averageMinutesPerDay;
        private double totalHours;
        private double completionRate;
        private List<SubjectTime> bySubject;
    }

    @Getter
    @Builder
    public static class MockExamSummary {
        private double averageScore;
        private int examCount;
        private String trend;  // UP, DOWN, STABLE
        private List<SubjectAverage> bySubject;
    }

    @Getter
    @Builder
    public static class AssignmentSummary {
        private double completionRate;
        private int totalAssignments;
        private int completedCount;
        private int overdueCount;
    }

    @Getter
    @Builder
    public static class TopStudentDto {
        private Long studentId;
        private String name;
        private double score;
        private String category;  // ATTENDANCE, STUDY_TIME, MOCK_EXAM
    }

    @Getter
    @Builder
    public static class AlertDto {
        private String type;  // WARNING, INFO
        private String message;
        private int studentCount;
    }
}
```

### DashboardService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.dto.dashboard.DashboardDataDto;
import com.reacademix.reacademix_backend.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class DashboardService {

    private final AttendanceRepository attendanceRepository;
    private final StudyTimeRepository studyTimeRepository;
    private final MockExamRepository mockExamRepository;
    private final AssignmentRepository assignmentRepository;
    private final StudentRepository studentRepository;

    public DashboardDataDto getDashboardData(String period, Long classId) {
        log.info("대시보드 데이터 조회: period={}, classId={}", period, classId);

        LocalDate endDate = LocalDate.now();
        LocalDate startDate = calculateStartDate(period, endDate);

        // 병렬로 데이터 수집
        CompletableFuture<DashboardDataDto.AttendanceSummary> attendanceFuture =
            CompletableFuture.supplyAsync(() -> getAttendanceSummary(classId, startDate, endDate));

        CompletableFuture<DashboardDataDto.StudyTimeSummary> studyTimeFuture =
            CompletableFuture.supplyAsync(() -> getStudyTimeSummary(classId, startDate, endDate));

        CompletableFuture<DashboardDataDto.MockExamSummary> mockExamFuture =
            CompletableFuture.supplyAsync(() -> getMockExamSummary(classId, startDate, endDate));

        CompletableFuture<DashboardDataDto.AssignmentSummary> assignmentFuture =
            CompletableFuture.supplyAsync(() -> getAssignmentSummary(classId, startDate, endDate));

        // 모든 데이터 수집 완료 대기
        CompletableFuture.allOf(attendanceFuture, studyTimeFuture, mockExamFuture, assignmentFuture).join();

        // 알림 생성
        List<DashboardDataDto.AlertDto> alerts = generateAlerts(
            attendanceFuture.join(), studyTimeFuture.join(), assignmentFuture.join());

        return DashboardDataDto.builder()
            .attendance(attendanceFuture.join())
            .studyTime(studyTimeFuture.join())
            .mockExam(mockExamFuture.join())
            .assignment(assignmentFuture.join())
            .alerts(alerts)
            .build();
    }

    private LocalDate calculateStartDate(String period, LocalDate endDate) {
        return switch (period) {
            case "daily" -> endDate;
            case "weekly" -> endDate.minusWeeks(1);
            case "monthly" -> endDate.minusMonths(1);
            default -> endDate.minusWeeks(1);
        };
    }

    private DashboardDataDto.AttendanceSummary getAttendanceSummary(
            Long classId, LocalDate startDate, LocalDate endDate) {
        Double avgRate = attendanceRepository.calculateAverageAttendanceRateByClass(
            classId, startDate, endDate);
        
        return DashboardDataDto.AttendanceSummary.builder()
            .averageRate(avgRate != null ? avgRate : 0.0)
            .totalStudents(studentRepository.countByClassroomId(classId))
            .build();
    }

    // 다른 Summary 메서드들도 유사하게 구현...

    private List<DashboardDataDto.AlertDto> generateAlerts(
            DashboardDataDto.AttendanceSummary attendance,
            DashboardDataDto.StudyTimeSummary studyTime,
            DashboardDataDto.AssignmentSummary assignment) {
        
        List<DashboardDataDto.AlertDto> alerts = new java.util.ArrayList<>();

        if (attendance.getAverageRate() < 80) {
            alerts.add(DashboardDataDto.AlertDto.builder()
                .type("WARNING")
                .message("평균 출석률이 80% 미만입니다.")
                .build());
        }

        if (assignment.getOverdueCount() > 0) {
            alerts.add(DashboardDataDto.AlertDto.builder()
                .type("WARNING")
                .message("마감 기한이 지난 과제가 " + assignment.getOverdueCount() + "건 있습니다.")
                .build());
        }

        return alerts;
    }
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-021
- Related Epic: Data Integration
