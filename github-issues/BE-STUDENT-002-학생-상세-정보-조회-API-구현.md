# 학생 상세 정보 조회 API 구현

- **Type**: Functional
- **Key**: BE-STUDENT-002
- **REQ / Epic**: REQ-FUNC-001
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-INFRA-003

## 📌 Description

학생 ID로 학생의 상세 정보를 조회하는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] GET /api/students/{studentId} 엔드포인트 구현
- [ ] GetStudentParamsDto 클래스 생성
- [ ] GetStudentResponseDto 클래스 생성
- [ ] StudentDetailDto 클래스 생성
- [ ] StudentsController.getStudent() 메서드 구현
- [ ] StudentsService.getStudent() 메서드 구현
- [ ] 존재하지 않는 studentId 시 404 반환
- [ ] API 응답 시간 500ms 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스
- 관련 엔티티: Student


## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-001
- Related Epic: Student Management
