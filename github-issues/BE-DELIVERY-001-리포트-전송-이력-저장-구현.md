# 리포트 전송 이력 저장 구현

- **Type**: Functional
- **Key**: BE-DELIVERY-001
- **REQ / Epic**: REQ-FUNC-028
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

리포트 전송 이력을 데이터베이스에 저장하는 기능을 구현합니다.

## ✅ Acceptance Criteria

- [ ] ReportDeliveryService.saveDeliveryHistory() 메서드 구현
- [ ] 리포트 ID, 학생 ID, 학부모 이메일, 전송 시간, 전송 성공/실패 여부 저장
- [ ] report_delivery 테이블에 전송 이력 저장
- [ ] 저장 완료 확인
- [ ] Firestore 저장 실패 시 에러 반환
- [ ] 필수 필드 누락 시 검증 에러 반환
- [ ] 저장 시간 1초 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Repository 레이어
- 관련 엔티티: Report, ReportDelivery
- 관련 테이블: report_delivery


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-09
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-028
- Related Epic: Report Delivery
