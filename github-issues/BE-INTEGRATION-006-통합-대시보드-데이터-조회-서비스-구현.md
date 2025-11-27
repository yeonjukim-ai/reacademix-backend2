# 통합 대시보드 데이터 조회 서비스 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-006
- **REQ / Epic**: REQ-FUNC-021
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

통합된 데이터를 대시보드 형태로 조회하는 서비스를 구현합니다. 출석률, 학습 시간, 모의고사 성적, 결제 현황을 집계합니다.

## ✅ Acceptance Criteria

- [ ] DashboardService.getDashboardData() 메서드 구현
- [ ] 기간별 데이터 조회 (daily, weekly, monthly)
- [ ] 출석률 집계
- [ ] 학습 시간 집계
- [ ] 모의고사 성적 집계
- [ ] 결제 현황 집계
- [ ] 테이블 형태로 데이터 구성
- [ ] 통합 대시보드 데이터 객체 반환
- [ ] 데이터 없을 시 빈 데이터 반환
- [ ] 처리 시간 500ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-021
- Related Epic: Data Integration
