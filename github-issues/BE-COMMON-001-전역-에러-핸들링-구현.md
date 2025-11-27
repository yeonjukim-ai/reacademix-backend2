# 전역 에러 핸들링 구현

- **Type**: Non-Functional
- **Key**: BE-COMMON-001
- **REQ / Epic**: REQ-NF-018
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-001

## 📌 Description

전역 예외 처리 핸들러를 구현하여 일관된 에러 응답 형식을 제공합니다. 사용자 친화적인 에러 메시지를 생성합니다.

## ✅ Acceptance Criteria

- [ ] @ControllerAdvice 클래스 생성
- [ ] 전역 예외 처리 핸들러 구현
- [ ] 에러 타입별 처리 (ValidationException, NotFoundException, UnauthorizedException 등)
- [ ] 사용자 친화적인 에러 메시지 생성
- [ ] 에러 코드 매핑
- [ ] 적절한 HTTP 상태 코드 반환
- [ ] 에러 응답 형식: { errorCode: string, message: string, details?: object }
- [ ] 모든 에러 로깅 (error 레벨)
- [ ] 에러 스택 트레이스 로깅 (개발 환경)
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- 구현 세부사항은 acceptance criteria 참조

## ⏱ 일정(Timeline)

- **Start**: 2025-11-30
- **End**: 2025-12-02
- **Lane**: Prerequisites
## 🔗 Traceability

- Related SRS: REQ-NF-018
- Related Epic: Common Infrastructure
