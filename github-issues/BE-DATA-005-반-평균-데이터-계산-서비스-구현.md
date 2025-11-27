# 반 평균 데이터 계산 서비스 구현

- **Type**: Functional
- **Key**: BE-DATA-005
- **REQ / Epic**: REQ-FUNC-007
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생이 속한 반의 평균 데이터를 계산하는 서비스를 구현합니다. MVP에서는 하드코딩된 반 평균값 또는 더미 데이터를 사용합니다.

## ✅ Acceptance Criteria

- [ ] ClassAverageService.getClassAverageData() 메서드 구현
- [ ] 하드코딩된 반 평균값 또는 더미 데이터 사용
- [ ] 학생 데이터와 반 평균 데이터 비교
- [ ] 차이값 산출 (학생 값 - 반 평균)
- [ ] 반 평균 데이터 반환 (출석률, 학습 시간, 모의고사 성적)
- [ ] 학생 ID 없을 시 기본값 반환
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-10
- **Lane**: Financial
## 🔗 Traceability

- Related SRS: REQ-FUNC-007
- Related Epic: Report Generation
