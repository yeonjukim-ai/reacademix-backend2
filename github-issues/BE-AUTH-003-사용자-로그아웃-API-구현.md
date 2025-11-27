# 사용자 로그아웃 API 구현

- **Type**: Functional
- **Key**: BE-AUTH-003
- **REQ / Epic**: REQ-FUNC-036
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002

## 📌 Description

사용자 로그아웃 API를 구현합니다. 토큰 무효화 처리를 수행합니다 (선택적: 토큰 블랙리스트 관리).

## ✅ Acceptance Criteria

- [ ] POST /api/auth/logout 엔드포인트 구현
- [ ] LogoutResponseDto 클래스 생성
- [ ] AuthController.logout() 메서드 구현
- [ ] AuthService.logout() 메서드 구현
- [ ] 토큰 무효화 처리 (선택적)
- [ ] 인증된 사용자만 접근 가능
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스

## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-16
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-036
- Related Epic: Authentication & Authorization
