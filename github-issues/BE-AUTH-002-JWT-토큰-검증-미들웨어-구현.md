# JWT 토큰 검증 미들웨어 구현

- **Type**: Functional
- **Key**: BE-AUTH-002
- **REQ / Epic**: REQ-FUNC-037
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-001

## 📌 Description

Spring Security를 사용하여 JWT 토큰 검증 미들웨어를 구현합니다. 모든 보호된 엔드포인트에 대해 토큰 검증을 수행하고, 유효하지 않은 토큰에 대해서는 401 Unauthorized를 반환합니다.

## ✅ Acceptance Criteria

- [ ] JWT 토큰 검증 필터 구현
- [ ] Spring Security 설정 구성
- [ ] 토큰 추출 로직 구현 (Authorization 헤더)
- [ ] 토큰 유효성 검증 로직 구현
- [ ] 토큰 만료 확인 로직 구현
- [ ] 사용자 정보 추출 및 SecurityContext 설정
- [ ] 토큰 없음 시 401 반환
- [ ] 토큰 만료 시 401 반환
- [ ] 토큰 무효 시 401 반환
- [ ] 인증 검증 시간 100ms 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- 구현 세부사항은 acceptance criteria 참조

## ⏱ 일정(Timeline)

- **Start**: 2025-12-12
- **End**: 2025-12-14
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-037
- Related Epic: Authentication & Authorization
