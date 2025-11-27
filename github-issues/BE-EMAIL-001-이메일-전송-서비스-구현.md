# 이메일 전송 서비스 구현

- **Type**: Functional
- **Key**: BE-EMAIL-001
- **REQ / Epic**: REQ-FUNC-041
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-REPORT-002

## 📌 Description

리포트 PDF를 이메일로 전송하는 서비스를 구현합니다. JavaMailSender 또는 외부 이메일 서비스 API (Resend, SendGrid)를 사용합니다.

## ✅ Acceptance Criteria

- [ ] 이메일 서비스 의존성 추가 (JavaMailSender 또는 외부 API 클라이언트)
- [ ] EmailService.sendReportEmail() 메서드 구현
- [ ] 이메일 서비스 API 호출 (Resend, SendGrid 등)
- [ ] 리포트 PDF를 이메일 첨부
- [ ] 이메일 전송 요청 수행
- [ ] 이메일 전송 실패 시 에러 반환
- [ ] 이메일 전송 처리 시간 5초 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- 관련 엔티티: Report


## ⏱ 일정(Timeline)

- **Start**: 2025-12-09
- **End**: 2025-12-12
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-041
- Related Epic: Report Delivery
