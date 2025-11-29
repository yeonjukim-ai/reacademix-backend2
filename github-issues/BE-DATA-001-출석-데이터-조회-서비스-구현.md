# 출석 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-001
- **REQ / Epic**: REQ-FUNC-003
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 출석 데이터를 조회하고 출석률을 계산하는 서비스를 구현합니다. 리포트 생성 시 출석 현황 섹션에 사용됩니다.

## ✅ Acceptance Criteria

### Service 구현
- [ ] `AttendanceService` 클래스 생성
- [ ] `getAttendanceData(studentId, startDate, endDate)` 메서드 구현
- [ ] `calculateAttendanceRate()` 메서드 구현

### 비즈니스 로직
- [ ] 기간별 출석 데이터 조회
- [ ] 출석률 계산: (출석 일수 / 전체 일수) × 100
- [ ] 상태별 집계 (출석, 결석, 지각, 조퇴)
- [ ] 날짜 기준 내림차순 정렬

### 성능 및 테스트
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### AttendanceDataDto.java

```java
package com.reacademix.reacademix_backend.dto.data;

import lombok.*;
import java.time.LocalDate;
import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AttendanceDataDto {
    private int totalDays;
    private int presentDays;
    private int absentDays;
    private int lateDays;
    private int earlyLeaveDays;
    private double attendanceRate;
    private List<DailyAttendance> dailyRecords;

    @Getter
    @Builder
    public static class DailyAttendance {
        private LocalDate date;
        private String status;
        private String checkInTime;
        private String checkOutTime;
    }
}
```

### AttendanceService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.attendance.Attendance;
import com.reacademix.reacademix_backend.domain.attendance.AttendanceStatus;
import com.reacademix.reacademix_backend.dto.data.AttendanceDataDto;
import com.reacademix.reacademix_backend.repository.AttendanceRepository;
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
public class AttendanceService {

    private final AttendanceRepository attendanceRepository;

    /**
     * 학생의 출석 데이터 조회 및 통계 계산
     */
    public AttendanceDataDto getAttendanceData(Long studentId, LocalDate startDate, LocalDate endDate) {
        log.debug("출석 데이터 조회: studentId={}, period={} ~ {}", studentId, startDate, endDate);

        List<Attendance> records = attendanceRepository
            .findByStudentIdAndAttendanceDateBetween(studentId, startDate, endDate);

        if (records.isEmpty()) {
            return AttendanceDataDto.builder()
                .totalDays(0)
                .presentDays(0)
                .absentDays(0)
                .lateDays(0)
                .earlyLeaveDays(0)
                .attendanceRate(0.0)
                .dailyRecords(List.of())
                .build();
        }

        // 상태별 집계
        Map<AttendanceStatus, Long> statusCount = records.stream()
            .collect(Collectors.groupingBy(Attendance::getStatus, Collectors.counting()));

        int totalDays = records.size();
        int presentDays = statusCount.getOrDefault(AttendanceStatus.PRESENT, 0L).intValue();
        int absentDays = statusCount.getOrDefault(AttendanceStatus.ABSENT, 0L).intValue();
        int lateDays = statusCount.getOrDefault(AttendanceStatus.LATE, 0L).intValue();
        int earlyLeaveDays = statusCount.getOrDefault(AttendanceStatus.EARLY_LEAVE, 0L).intValue();

        // 출석률 계산 (출석 + 지각도 출석으로 간주)
        double attendanceRate = totalDays > 0 
            ? ((presentDays + lateDays) * 100.0) / totalDays 
            : 0.0;

        // 일별 기록 변환
        List<AttendanceDataDto.DailyAttendance> dailyRecords = records.stream()
            .sorted((a, b) -> b.getAttendanceDate().compareTo(a.getAttendanceDate()))
            .map(a -> AttendanceDataDto.DailyAttendance.builder()
                .date(a.getAttendanceDate())
                .status(a.getStatus().name())
                .checkInTime(a.getCheckInTime() != null ? a.getCheckInTime().toString() : null)
                .checkOutTime(a.getCheckOutTime() != null ? a.getCheckOutTime().toString() : null)
                .build())
            .collect(Collectors.toList());

        return AttendanceDataDto.builder()
            .totalDays(totalDays)
            .presentDays(presentDays)
            .absentDays(absentDays)
            .lateDays(lateDays)
            .earlyLeaveDays(earlyLeaveDays)
            .attendanceRate(Math.round(attendanceRate * 10) / 10.0)
            .dailyRecords(dailyRecords)
            .build();
    }
}
```

---

## 📝 구현 체크리스트

- [ ] `AttendanceDataDto` 생성
- [ ] `AttendanceService` 구현
- [ ] Repository 메서드 확인
- [ ] 단위 테스트 작성

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial

## 🔗 Traceability

- Related SRS: REQ-FUNC-003
- Related Epic: Report Generation
