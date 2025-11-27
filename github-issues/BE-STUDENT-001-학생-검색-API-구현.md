# 학생 검색 API 구현

- **Type**: Functional
- **Key**: BE-STUDENT-001
- **REQ / Epic**: REQ-FUNC-001
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-INFRA-003

## 📌 Description

학생 이름 또는 학생 ID로 학생을 검색하는 API를 구현합니다. 부분 일치 검색을 지원하고, 페이지네이션을 제공합니다.

## ✅ Acceptance Criteria

- [ ] GET /api/students 엔드포인트 구현
- [ ] GetStudentsQueryDto 클래스 생성 (search, page, limit 필드)
- [ ] GetStudentsResponseDto 클래스 생성 (students, total, page 필드)
- [ ] StudentDto 클래스 생성
- [ ] StudentsController.getStudents() 메서드 구현
- [ ] StudentsService.getStudents() 메서드 구현 (부분 일치 검색, 페이지네이션)
- [ ] 검색 결과 최대 50명 제한
- [ ] 페이지네이션 기본값: page=1, limit=20
- [ ] 빈 검색 쿼리 시 빈 목록 반환
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
