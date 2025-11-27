# 리포트 전송 이력 조회 API 구현

- **Type**: Functional
- **Key**: BE-DELIVERY-002
- **REQ / Epic**: REQ-FUNC-028
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-DELIVERY-001

## 📌 Description

리포트 전송 이력을 조회하는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] GET /api/reports/delivery/history 엔드포인트 구현
- [ ] GetDeliveryHistoryQueryDto 클래스 생성 (studentId, page, limit 필드)
- [ ] GetDeliveryHistoryResponseDto 클래스 생성 (deliveries, total 필드)
- [ ] DeliveryHistoryDto 클래스 생성
- [ ] ReportsController.getDeliveryHistory() 메서드 구현
- [ ] ReportsService.getDeliveryHistory() 메서드 구현
- [ ] studentId 필터링 (선택적)
- [ ] 전송 시간 기준 내림차순 정렬
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

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-028
- Related Epic: Report Delivery
