# 학습 시간 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-002
- **REQ / Epic**: REQ-FUNC-004
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 학습 시간 데이터를 조회하고 집계하는 서비스를 구현합니다. 일평균, 주평균, 목표 대비 달성률을 계산합니다.

## ✅ Acceptance Criteria

- [ ] StudyTimeService.getStudyTimeData() 메서드 구현
- [ ] 일평균 학습 시간 계산: (전체 학습 시간 합계 / 학습 일수)
- [ ] 주평균 학습 시간 계산: (전체 학습 시간 합계 / 주 수)
- [ ] 목표 대비 달성률 계산: (실제 평균 / 목표) × 100
- [ ] 날짜 기준 내림차순 정렬
- [ ] 학습 시간 데이터 배열 반환 (date, hours)
- [ ] 학습 시간 데이터 없을 시 평균 0, 달성률 0% 반환
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- 관련 엔티티: StudyTime


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial
## 🔗 Traceability

- Related SRS: REQ-FUNC-004
- Related Epic: Report Generation
