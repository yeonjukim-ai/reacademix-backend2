# 사용자 인증 API 구현 - 로그인

- **Type**: Functional
- **Key**: BE-AUTH-001
- **REQ / Epic**: REQ-FUNC-036
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

사용자 로그인 API를 구현합니다. 이메일과 비밀번호를 받아 인증을 수행하고, JWT 토큰을 발급합니다. 비밀번호는 bcrypt로 암호화하여 저장하고 검증합니다.

## ✅ Acceptance Criteria

- [ ] POST /api/auth/login 엔드포인트 구현
- [ ] LoginRequestDto 클래스 생성 (email, password 필드)
- [ ] LoginResponseDto 클래스 생성 (token, user 필드)
- [ ] AuthController.login() 메서드 구현
- [ ] AuthService.login() 메서드 구현 (이메일/비밀번호 검증, JWT 토큰 생성)
- [ ] 비밀번호 암호화 (bcrypt) 구현
- [ ] JWT 토큰 생성 및 발급 (유효기간 24시간)
- [ ] 인증 실패 시 적절한 에러 응답 (401)
- [ ] 요청 데이터 검증 (이메일 형식, 비밀번호 최소 길이)
- [ ] API 응답 시간 500ms 이내
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-11
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-036
- Related Epic: Authentication & Authorization
