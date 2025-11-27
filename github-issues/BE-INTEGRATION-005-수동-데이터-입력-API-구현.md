# 수동 데이터 입력 API 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-005
- **REQ / Epic**: REQ-FUNC-016
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-INTEGRATION-002, BE-INTEGRATION-004

## 📌 Description

사용자가 수동으로 데이터를 입력할 수 있는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] POST /api/integrations/manual 엔드포인트 구현
- [ ] ManualDataInputRequestDto 클래스 생성 (systemType, data 필드)
- [ ] ManualDataInputResponseDto 클래스 생성 (status 필드)
- [ ] IntegrationsController.manualInput() 메서드 구현
- [ ] IntegrationsService.manualInput() 메서드 구현
- [ ] 데이터 검증 서비스 호출
- [ ] 데이터 즉시 저장
- [ ] 실시간 저장 완료 확인
- [ ] 데이터 검증 실패 시 검증 오류 반환
- [ ] 필수 필드 누락 시 검증 에러 반환
- [ ] API 응답 시간 500ms 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스


## ⏱ 일정(Timeline)

- **Start**: 2025-12-13
- **End**: 2025-12-15
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-016
- Related Epic: Data Integration
