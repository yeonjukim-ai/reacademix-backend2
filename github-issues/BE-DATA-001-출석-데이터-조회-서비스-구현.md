# 출석 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-001
- **REQ / Epic**: REQ-FUNC-003
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 출석 데이터를 조회하고 출석률을 계산하는 서비스를 구현합니다. 전체 기간 및 최근 4주 출석률을 계산합니다.

## ✅ Acceptance Criteria

- [ ] AttendanceService.getAttendanceData() 메서드 구현
- [ ] 전체 기간 출석률 계산: (출석 일수 / 전체 수업 일수) × 100
- [ ] 최근 4주 출석률 계산
- [ ] 날짜 기준 내림차순 정렬
- [ ] 출석 데이터 배열 반환 (date, isPresent)
- [ ] 출석 데이터 없을 시 출석률 0% 반환
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- 관련 엔티티: Attendance

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial
## 🔗 Traceability

- Related SRS: REQ-FUNC-003
- Related Epic: Report Generation
