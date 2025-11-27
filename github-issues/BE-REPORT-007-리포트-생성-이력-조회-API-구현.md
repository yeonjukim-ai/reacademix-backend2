# 리포트 생성 이력 조회 API 구현

- **Type**: Functional
- **Key**: BE-REPORT-007
- **REQ / Epic**: REQ-FUNC-013
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-REPORT-005

## 📌 Description

리포트 생성 이력을 조회하는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] GET /api/reports/history 엔드포인트 구현
- [ ] GetReportsHistoryQueryDto 클래스 생성 (studentId, page, limit 필드)
- [ ] GetReportsHistoryResponseDto 클래스 생성 (reports, total 필드)
- [ ] ReportHistoryDto 클래스 생성
- [ ] ReportsController.getReportsHistory() 메서드 구현
- [ ] ReportsService.getReportsHistory() 메서드 구현
- [ ] studentId 필터링 (선택적)
- [ ] 생성 시간 기준 내림차순 정렬
- [ ] 페이지네이션 적용
- [ ] API 응답 시간 500ms 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스
- 관련 엔티티: Report


## ⏱ 일정(Timeline)

- **Start**: 2025-12-27
- **End**: 2025-12-29
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-013
- Related Epic: Report Generation
