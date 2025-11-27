# 통합 대시보드 조회 API 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-007
- **REQ / Epic**: REQ-FUNC-021
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-INTEGRATION-006

## 📌 Description

통합 대시보드 데이터를 조회하는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] GET /api/integrations/dashboard 엔드포인트 구현
- [ ] GetDashboardQueryDto 클래스 생성 (period 필드)
- [ ] GetDashboardResponseDto 클래스 생성 (attendance, studyTime, mockExam, payment 필드)
- [ ] 각 DashboardDto 클래스 생성
- [ ] IntegrationsController.getDashboard() 메서드 구현
- [ ] 대시보드 서비스 호출
- [ ] period 값 검증
- [ ] API 응답 시간 500ms 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스


## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-021
- Related Epic: Data Integration
