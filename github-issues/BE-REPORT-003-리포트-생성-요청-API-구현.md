# 리포트 생성 요청 API 구현

- **Type**: Functional
- **Key**: BE-REPORT-003
- **REQ / Epic**: REQ-FUNC-002
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-DATA-001, BE-DATA-002, BE-DATA-003, BE-DATA-004, BE-DATA-005, BE-INSIGHT-001, BE-REPORT-002

## 📌 Description

리포트 생성 요청을 받아 처리하는 API를 구현합니다. 리포트 생성 프로세스를 시작하고, 진행 상태를 반환합니다. 비동기 처리를 고려합니다.

## ✅ Acceptance Criteria

- [ ] POST /api/reports/generate 엔드포인트 구현
- [ ] GenerateReportRequestDto 클래스 생성 (studentId, format 필드)
- [ ] GenerateReportResponseDto 클래스 생성 (reportId, downloadUrl, status 필드)
- [ ] ReportsController.generateReport() 메서드 구현
- [ ] ReportsService.generateReport() 메서드 구현
- [ ] 리포트 생성 프로세스 시작 (비동기 또는 동기)
- [ ] reportId 생성
- [ ] 진행 상태 설정 (processing)
- [ ] 존재하지 않는 studentId 시 404 반환
- [ ] 중복 요청 처리
- [ ] 리포트 생성 요청 API 응답 시간 1초 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스
- 관련 엔티티: Report

## ⏱ 일정(Timeline)

- **Start**: 2025-12-19
- **End**: 2025-12-24
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-002
- Related Epic: Report Generation
