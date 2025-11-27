# 모의고사 성적 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-003
- **REQ / Epic**: REQ-FUNC-005
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생의 모의고사 성적 데이터를 조회하고 분석하는 서비스를 구현합니다. 최근 5회 모의고사 성적을 조회하고 추이 분석 및 등급 변화를 계산합니다.

## ✅ Acceptance Criteria

- [ ] MockExamService.getMockExamData() 메서드 구현
- [ ] 최근 5회 모의고사 성적 필터링
- [ ] 시험 날짜 기준 내림차순 정렬
- [ ] 추이 분석 수행 (상승/하락/유지)
- [ ] 등급 변화 분석 (등급 상승/하락 판단)
- [ ] 모의고사 성적 배열 반환 (examRound, score, grade, examDate)
- [ ] 모의고사 데이터 5회 미만 시 존재하는 데이터만 반환
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- 관련 엔티티: MockExam


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Financial
## 🔗 Traceability

- Related SRS: REQ-FUNC-005
- Related Epic: Report Generation
