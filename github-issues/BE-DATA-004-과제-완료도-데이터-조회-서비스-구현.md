# 과제 완료도 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-004
- **REQ / Epic**: REQ-FUNC-006
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 과제 완료도 데이터를 조회하는 서비스를 구현합니다. 완료율을 계산하고 미완료 과제 목록을 반환합니다.

## ✅ Acceptance Criteria

- [ ] AssignmentService.getAssignmentData() 메서드 구현
- [ ] 완료율 계산: (완료한 과제 수 / 전체 과제 수) × 100
- [ ] 미완료 과제 목록 필터링 (최대 10개)
- [ ] 마감일 기준 내림차순 정렬
- [ ] 과제 데이터 배열 반환 (assignmentName, isCompleted, dueDate)
- [ ] 과제 데이터 없을 시 완료율 0% 반환
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- 관련 엔티티: Assignment


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial
## 🔗 Traceability

- Related SRS: REQ-FUNC-006
- Related Epic: Report Generation
