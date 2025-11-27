# Git 커밋 & PR 템플릿

## 1. 커밋 메시지

### 첫 커밋 (회원가입 기능 스켈레톤)

```
feat: add user signup API skeleton (#1)

- Add User entity with JPA annotations
- Add UserRepository interface
- Add UserService with signup business logic
- Add UserController with POST /api/v1/users endpoint
- Add DTOs (UserSignupRequest, UserResponse)
- Add BaseTimeEntity for timestamp management
- Add SecurityConfig for PasswordEncoder
- Add JpaAuditingConfig for automatic timestamp

Related to: BE-AUTH-001
```

### 대안 (더 간결한 버전)

```
feat: implement user signup API (#1)

- User entity, repository, service, controller
- Password encryption with bcrypt
- Email duplicate validation
- Request/Response DTOs

Closes #1
```

---

## 2. Pull Request 템플릿

### PR 제목

```
feat: Add user signup API implementation (#1)
```

### PR 본문

```markdown
## 📋 요약

사용자 회원가입 API를 구현했습니다. 이메일과 비밀번호를 받아 사용자를 등록하고, 비밀번호는 bcrypt로 암호화하여 저장합니다.

**API 엔드포인트**: `POST /api/v1/users`

## 🔄 변경 사항

### 추가된 파일

#### Entity & Domain
- `src/main/java/.../domain/user/User.java` - User JPA 엔티티
- `src/main/java/.../domain/user/UserRole.java` - 사용자 역할 Enum
- `src/main/java/.../domain/user/UserStatus.java` - 사용자 상태 Enum
- `src/main/java/.../common/BaseTimeEntity.java` - 공통 타임스탬프 엔티티

#### Repository
- `src/main/java/.../repository/UserRepository.java` - User 데이터 접근 인터페이스

#### Service
- `src/main/java/.../service/UserService.java` - 회원가입 비즈니스 로직

#### Controller
- `src/main/java/.../controller/UserController.java` - 회원가입 REST API

#### DTO
- `src/main/java/.../dto/request/UserSignupRequest.java` - 회원가입 요청 DTO
- `src/main/java/.../dto/response/UserResponse.java` - 회원가입 응답 DTO

#### Config
- `src/main/java/.../config/SecurityConfig.java` - PasswordEncoder Bean 설정
- `src/main/java/.../config/JpaAuditingConfig.java` - JPA Auditing 설정

#### Documentation
- `docs/api-spec-auth.md` - API 명세서
- `docs/user-data-model.md` - 데이터 모델 설계 (ERD)
- `docs/user-class-diagram.md` - 클래스 다이어그램
- `docs/user-code-snippets.md` - 코드 스니펫 문서

### 주요 기능

1. **회원가입 API**
   - 이메일, 비밀번호, 이름을 받아 사용자 등록
   - 이메일 중복 검사
   - 비밀번호 bcrypt 암호화 (salt rounds: 10)
   - 기본 역할: ADMIN, 기본 상태: ACTIVE

2. **데이터 검증**
   - 이메일 형식 검증
   - 비밀번호 길이 검증 (최소 8자)
   - 이름 길이 검증 (최소 2자)

3. **자동 타임스탬프**
   - `createdAt`, `updatedAt` 자동 관리 (JPA Auditing)

## 🧪 테스트 방법

### 1. API 테스트 (Postman/curl)

```bash
# 회원가입 요청
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "테스트 사용자"
  }'
```

**예상 응답 (201 Created):**
```json
{
  "userId": 1,
  "email": "test@example.com",
  "name": "테스트 사용자",
  "createdAt": "2025-01-27T10:30:00"
}
```

### 2. 이메일 중복 테스트

동일한 이메일로 두 번 요청 시 에러 발생 확인

### 3. 검증 실패 테스트

- 잘못된 이메일 형식
- 8자 미만 비밀번호
- 2자 미만 이름

## 📚 관련 문서

- [API 명세서](./docs/api-spec-auth.md)
- [데이터 모델 설계](./docs/user-data-model.md)
- [클래스 다이어그램](./docs/user-class-diagram.md)
- [코드 스니펫](./docs/user-code-snippets.md)

## 🔗 관련 이슈

Closes #1

**참조:**
- SRS: REQ-FUNC-036 (사용자 인증)
- GitHub Issue: #1 - BE-AUTH-001

## ⚠️ 주의사항

- 아직 테스트 코드는 포함되지 않았습니다 (다음 PR에서 추가 예정)
- 커스텀 예외 처리는 아직 구현되지 않았습니다 (전역 예외 핸들러 구현 후 개선 예정)
- 의존성 추가 필요: Spring Boot Web, Data JPA, Security, Validation, Lombok

## 📝 TODO (다음 단계)

- [ ] 단위 테스트 작성 (Service, Repository)
- [ ] 통합 테스트 작성 (Controller)
- [ ] 커스텀 예외 클래스 추가
- [ ] 전역 예외 핸들러 구현
- [ ] Swagger/OpenAPI 문서화
```

---

## 3. GitHub Issue 코멘트

### Issue #1 (BE-AUTH-001) 코멘트

```markdown
## ✅ 회원가입 기능 구현 완료

회원가입 API 구현을 완료했습니다. 주요 설계 결정사항과 구현 내용을 정리합니다.

### 📐 주요 설계 결정

#### 1. API 설계
- **엔드포인트**: `POST /api/v1/users`
- **요청 DTO**: `UserSignupRequest` (email, password, name)
- **응답 DTO**: `UserResponse` (userId, email, name, createdAt)
- **상세 명세**: [API 명세서](./docs/api-spec-auth.md)

#### 2. 데이터 모델 설계
- **ERD**: User 엔티티 중심 설계
- **테이블**: `users` (id, email, password, name, role, status, created_at, updated_at)
- **인덱스**: email (UNIQUE), status, role
- **상세 설계**: [데이터 모델 설계](./docs/user-data-model.md)

#### 3. 클래스 구조 설계
- **레이어**: Controller → Service → Repository
- **주요 클래스**: UserController, UserService, UserRepository, User (Entity)
- **상세 설계**: [클래스 다이어그램](./docs/user-class-diagram.md)

### 🛠️ 구현 내용

#### 완료된 항목
- ✅ User JPA 엔티티 생성 (Lombok 사용)
- ✅ UserRepository 인터페이스 (findByEmail, existsByEmail)
- ✅ UserService.signup() 메서드 구현
  - 이메일 중복 검사
  - 비밀번호 bcrypt 암호화
  - User 엔티티 생성/저장
- ✅ UserController 회원가입 엔드포인트 구현
- ✅ DTO 클래스 (UserSignupRequest, UserResponse)
- ✅ BaseTimeEntity (자동 타임스탬프 관리)
- ✅ SecurityConfig (PasswordEncoder Bean)
- ✅ JpaAuditingConfig (JPA Auditing 활성화)

#### 코드 위치
- Entity: `src/main/java/.../domain/user/User.java`
- Repository: `src/main/java/.../repository/UserRepository.java`
- Service: `src/main/java/.../service/UserService.java`
- Controller: `src/main/java/.../controller/UserController.java`
- DTO: `src/main/java/.../dto/request/UserSignupRequest.java`, `.../dto/response/UserResponse.java`

### 📚 관련 문서

- [API 명세서](./docs/api-spec-auth.md)
- [데이터 모델 설계 (ERD)](./docs/user-data-model.md)
- [클래스 다이어그램 (CLD)](./docs/user-class-diagram.md)
- [코드 스니펫](./docs/user-code-snippets.md)

### 🔗 Pull Request

PR: #<PR_NUMBER>

### 📝 다음 단계

- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성
- [ ] 커스텀 예외 처리 (EmailDuplicateException 등)
- [ ] 전역 예외 핸들러 구현
- [ ] 로그인 API 구현 (BE-AUTH-001의 나머지 부분)
```

---

## 4. 커밋 메시지 가이드 (참고)

### Conventional Commits 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 종류
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드 설정, 의존성 추가 등

### 예시

```
feat(auth): add user signup API (#1)

- Implement User entity with JPA annotations
- Add UserService with signup business logic
- Add UserController with POST /api/v1/users endpoint
- Add password encryption with bcrypt

Closes #1
```

---

**작성일**: 2025-01-27  
**버전**: 1.0

