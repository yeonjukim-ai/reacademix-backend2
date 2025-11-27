# 리포트 다운로드 API 구현

- **Type**: Functional
- **Key**: BE-REPORT-006
- **REQ / Epic**: REQ-FUNC-012
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-REPORT-003

## 📌 Description

생성된 리포트를 다운로드할 수 있는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] GET /api/reports/{reportId}/download 엔드포인트 구현
- [ ] DownloadReportParamsDto 클래스 생성
- [ ] ReportsController.downloadReport() 메서드 구현
- [ ] ReportsService.downloadReport() 메서드 구현
- [ ] 리포트 정보 조회
- [ ] PDF 파일 다운로드 URL 생성 또는 파일 스트림 반환
- [ ] Content-Type: application/pdf 설정
- [ ] Content-Disposition 헤더 설정
- [ ] 존재하지 않는 reportId 시 404 반환
- [ ] 파일 없을 시 404 반환
- [ ] API 응답 시간 500ms 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스
- 관련 엔티티: Report


## ⏱ 일정(Timeline)

- **Start**: 2025-12-25
- **End**: 2025-12-27
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-012
- Related Epic: Report Generation
