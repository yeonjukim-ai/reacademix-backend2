# 수동 리포트 이메일 전송 API 구현

- **Type**: Functional
- **Key**: BE-EMAIL-002
- **REQ / Epic**: REQ-FUNC-041
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-EMAIL-001, BE-REPORT-003, BE-DELIVERY-001

## 📌 Description

리포트 생성 후 수동으로 이메일 전송을 수행하는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] POST /api/reports/{reportId}/send-email 엔드포인트 구현
- [ ] SendReportEmailRequestDto 클래스 생성 (parentEmail 필드)
- [ ] SendReportEmailParamsDto 클래스 생성 (reportId 필드)
- [ ] SendReportEmailResponseDto 클래스 생성 (deliveryId, status 필드)
- [ ] ReportsController.sendReportEmail() 메서드 구현
- [ ] ReportsService.sendReportEmail() 메서드 구현
- [ ] 리포트 정보 조회
- [ ] 리포트 PDF 다운로드
- [ ] 이메일 전송 서비스 호출
- [ ] 리포트 전송 이력 저장
- [ ] 존재하지 않는 reportId 시 404 반환
- [ ] 파일 없을 시 404 반환
- [ ] 이메일 형식 검증
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스
- 관련 엔티티: Report


## ⏱ 일정(Timeline)

- **Start**: 2025-12-25
- **End**: 2025-12-28
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-041
- Related Epic: Report Delivery
