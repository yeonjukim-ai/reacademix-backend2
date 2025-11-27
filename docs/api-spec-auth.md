# 사용자 인증 API 명세서

## 개요

본 문서는 ReAcademix Backend의 사용자 인증 관련 API 명세서입니다. 
Issue #1 (BE-AUTH-001) "사용자 인증 API 구현 - 로그인"을 구현하기 위한 상세 설계를 포함합니다.

**참조 문서:**
- SRS: REQ-FUNC-036 (사용자 인증)
- GitHub Issue: #1 - BE-AUTH-001

---

## 1. 회원가입 API

### 1.1 Endpoint

```
POST /api/v1/users
```

### 1.2 Request Body

| 필드명 | 타입 | 필수 여부 | 검증 규칙 | 설명 |
|--------|------|----------|----------|------|
| `email` | String | 필수 | - 이메일 형식 검증 (RFC 5322)<br/>- 최대 255자<br/>- 중복 불가 | 사용자 이메일 주소 (로그인 ID로 사용) |
| `password` | String | 필수 | - 최소 8자 이상<br/>- 최대 128자<br/>- 영문, 숫자, 특수문자 중 2종류 이상 포함 권장 | 사용자 비밀번호 (평문, 서버에서 암호화 저장) |
| `name` | String | 필수 | - 최소 2자 이상<br/>- 최대 100자<br/>- 한글, 영문, 숫자, 공백 허용 | 사용자 이름 |

### 1.3 Request Body 예시

```json
{
  "email": "admin@academy.com",
  "password": "SecurePass123!",
  "name": "관리자"
}
```

### 1.4 Response Body

#### 성공 응답 (201 Created)

```json
{
  "success": true,
  "data": {
    "userId": "usr-001",
    "email": "admin@academy.com",
    "name": "관리자",
    "createdAt": "2025-01-27T10:30:00Z"
  },
  "message": "회원가입이 완료되었습니다."
}
```

#### 에러 응답 (400 Bad Request - 이메일 중복)

```json
{
  "success": false,
  "error": {
    "code": "AUTH_001",
    "message": "이미 등록된 이메일입니다.",
    "details": {
      "field": "email",
      "rejectedValue": "admin@academy.com"
    }
  },
  "timestamp": "2025-01-27T10:30:00Z"
}
```

#### 에러 응답 (400 Bad Request - 검증 실패)

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_001",
    "message": "입력 데이터 검증에 실패했습니다.",
    "details": {
      "errors": [
        {
          "field": "email",
          "message": "올바른 이메일 형식이 아닙니다."
        },
        {
          "field": "password",
          "message": "비밀번호는 최소 8자 이상이어야 합니다."
        }
      ]
    }
  },
  "timestamp": "2025-01-27T10:30:00Z"
}
```

### 1.5 업무 규칙

1. **이메일 중복 검사**
   - 회원가입 시 `users` 테이블에서 동일한 이메일이 존재하는지 확인
   - 중복된 경우 `AUTH_001` 에러 코드와 함께 400 Bad Request 반환
   - 이메일은 대소문자 구분 없이 비교 (소문자로 정규화하여 저장)

2. **비밀번호 암호화**
   - 평문 비밀번호를 bcrypt 알고리즘으로 암호화하여 저장
   - bcrypt salt rounds: 10 이상 권장 (보안 강화)
   - 암호화된 비밀번호는 `users.password` 필드에 저장
   - 평문 비밀번호는 메모리에서 즉시 제거

3. **기본 Role/Status 값**
   - MVP에서는 단일 관리자 역할만 지원 (역할 구분 제외)
   - 모든 사용자는 동일한 권한을 가짐
   - 사용자 상태는 별도 관리하지 않음 (활성 상태로 가정)

4. **사용자 ID 생성**
   - UUID v4 형식 사용 (예: `usr-001`, `usr-550e8400-e29b-41d4-a716-446655440000`)
   - 또는 데이터베이스 자동 생성 (AUTO_INCREMENT 또는 UUID)

### 1.6 예외 케이스

| HTTP 상태 코드 | 에러 코드 | 상황 | 메시지 |
|---------------|----------|------|--------|
| 400 | `VALIDATION_001` | 요청 데이터 검증 실패 | "입력 데이터 검증에 실패했습니다." |
| 400 | `AUTH_001` | 이메일 중복 | "이미 등록된 이메일입니다." |
| 400 | `VALIDATION_002` | 이메일 형식 오류 | "올바른 이메일 형식이 아닙니다." |
| 400 | `VALIDATION_003` | 비밀번호 길이 부족 | "비밀번호는 최소 8자 이상이어야 합니다." |
| 400 | `VALIDATION_004` | 이름 길이 부족 | "이름은 최소 2자 이상이어야 합니다." |
| 500 | `SYSTEM_001` | 데이터베이스 오류 | "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요." |
| 500 | `SYSTEM_002` | 비밀번호 암호화 실패 | "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요." |

---

## 2. 로그인 API

### 2.1 Endpoint

```
POST /api/v1/auth/login
```

### 2.2 Request Body

| 필드명 | 타입 | 필수 여부 | 검증 규칙 | 설명 |
|--------|------|----------|----------|------|
| `email` | String | 필수 | - 이메일 형식 검증<br/>- 최대 255자 | 사용자 이메일 주소 |
| `password` | String | 필수 | - 최소 8자 이상<br/>- 최대 128자 | 사용자 비밀번호 (평문) |

### 2.3 Request Body 예시

```json
{
  "email": "admin@academy.com",
  "password": "SecurePass123!"
}
```

### 2.4 Response Body

#### 성공 응답 (200 OK)

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3ItMDAxIiwiaWF0IjoxNzA2MzQ1ODAwLCJleHAiOjE3MDY0MzIyMDB9.example",
    "tokenType": "Bearer",
    "expiresIn": 86400,
    "user": {
      "userId": "usr-001",
      "email": "admin@academy.com",
      "name": "관리자"
    }
  },
  "message": "로그인에 성공했습니다."
}
```

#### 에러 응답 (401 Unauthorized - 이메일 없음)

```json
{
  "success": false,
  "error": {
    "code": "AUTH_002",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
    "details": null
  },
  "timestamp": "2025-01-27T10:30:00Z"
}
```

#### 에러 응답 (401 Unauthorized - 비밀번호 불일치)

```json
{
  "success": false,
  "error": {
    "code": "AUTH_003",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
    "details": null
  },
  "timestamp": "2025-01-27T10:30:00Z"
}
```

### 2.5 업무 규칙

1. **이메일/비밀번호 검증**
   - `users` 테이블에서 이메일로 사용자 조회
   - 사용자가 존재하지 않으면 `AUTH_002` 에러 반환 (보안상 구체적인 이유는 명시하지 않음)
   - 저장된 암호화된 비밀번호와 입력된 평문 비밀번호를 bcrypt로 비교
   - 비밀번호가 일치하지 않으면 `AUTH_003` 에러 반환

2. **JWT 토큰 생성**
   - 인증 성공 시 JWT 토큰 생성
   - 토큰 페이로드:
     - `sub`: 사용자 ID (userId)
     - `email`: 사용자 이메일
     - `iat`: 토큰 발급 시간 (issued at)
     - `exp`: 토큰 만료 시간 (expiration, 발급 후 24시간)
   - 토큰 유효기간: 24시간 (86400초)
   - 토큰 타입: Bearer

3. **응답 시간 제한**
   - API 응답 시간: 평균 500ms 이내 (REQ-NF-005)
   - 데이터베이스 쿼리 최적화 필요

4. **보안 고려사항**
   - 로그인 실패 시 구체적인 실패 이유를 명시하지 않음 (이메일 없음/비밀번호 불일치 구분하지 않음)
   - 무차별 대입 공격 방지를 위한 로그인 시도 횟수 제한 고려 (Post-MVP)

### 2.6 예외 케이스

| HTTP 상태 코드 | 에러 코드 | 상황 | 메시지 |
|---------------|----------|------|--------|
| 400 | `VALIDATION_001` | 요청 데이터 검증 실패 | "입력 데이터 검증에 실패했습니다." |
| 400 | `VALIDATION_002` | 이메일 형식 오류 | "올바른 이메일 형식이 아닙니다." |
| 400 | `VALIDATION_003` | 비밀번호 길이 부족 | "비밀번호는 최소 8자 이상이어야 합니다." |
| 401 | `AUTH_002` | 이메일 없음 | "이메일 또는 비밀번호가 올바르지 않습니다." |
| 401 | `AUTH_003` | 비밀번호 불일치 | "이메일 또는 비밀번호가 올바르지 않습니다." |
| 500 | `SYSTEM_001` | 데이터베이스 오류 | "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요." |
| 500 | `SYSTEM_003` | JWT 토큰 생성 실패 | "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요." |

---

## 3. 공통 에러 응답 구조

모든 API는 다음 공통 에러 응답 형식을 사용합니다:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적인 에러 메시지",
    "details": {
      // 에러별 상세 정보 (선택적)
      "field": "필드명",
      "rejectedValue": "거부된 값",
      "errors": [
        {
          "field": "필드명",
          "message": "필드별 에러 메시지"
        }
      ]
    }
  },
  "timestamp": "2025-01-27T10:30:00Z"
}
```

### 에러 코드 규칙

- `AUTH_XXX`: 인증 관련 에러
- `VALIDATION_XXX`: 데이터 검증 관련 에러
- `SYSTEM_XXX`: 시스템 오류

---

## 4. 요약 표

### 4.1 회원가입 API

| 항목 | 내용 |
|------|------|
| **Endpoint** | `POST /api/v1/users` |
| **Request** | `{ "email": string, "password": string, "name": string }` |
| **Response (성공)** | `201 Created` - `{ "success": true, "data": { "userId", "email", "name", "createdAt" } }` |
| **Response (에러)** | `400 Bad Request` - 이메일 중복, 검증 실패<br/>`500 Internal Server Error` - 시스템 오류 |
| **주요 업무 규칙** | 이메일 중복 검사, 비밀번호 bcrypt 암호화, 기본 Role 없음 (단일 권한) |

### 4.2 로그인 API

| 항목 | 내용 |
|------|------|
| **Endpoint** | `POST /api/v1/auth/login` |
| **Request** | `{ "email": string, "password": string }` |
| **Response (성공)** | `200 OK` - `{ "success": true, "data": { "token", "tokenType", "expiresIn", "user" } }` |
| **Response (에러)** | `401 Unauthorized` - 이메일 없음, 비밀번호 불일치<br/>`400 Bad Request` - 검증 실패<br/>`500 Internal Server Error` - 시스템 오류 |
| **주요 업무 규칙** | 이메일/비밀번호 검증, JWT 토큰 발급 (24시간 유효), 응답 시간 500ms 이내 |

---

## 5. 구현 고려사항

### 5.1 기술 스택

- **Spring Boot**: 4.0.0
- **Spring Security**: JWT 토큰 검증 및 인증
- **Spring Data JPA**: 데이터베이스 접근
- **bcrypt**: 비밀번호 암호화
- **JJWT**: JWT 토큰 생성 및 검증

### 5.2 데이터베이스 스키마

```sql
CREATE TABLE users (
  user_id VARCHAR(36) PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL, -- bcrypt 해시
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### 5.3 보안 고려사항

1. **비밀번호 암호화**: bcrypt 사용 (salt rounds ≥ 10)
2. **JWT 토큰**: HS256 알고리즘 사용, 시크릿 키는 환경 변수로 관리
3. **HTTPS**: 모든 통신은 HTTPS 사용 (REQ-NF-015)
4. **에러 메시지**: 보안을 위해 구체적인 실패 이유를 노출하지 않음

### 5.4 성능 요구사항

- **회원가입 API**: 평균 응답 시간 500ms 이내
- **로그인 API**: 평균 응답 시간 500ms 이내 (REQ-NF-005)
- **데이터베이스 쿼리**: 인덱스 활용하여 최적화

---

## 6. 테스트 시나리오

### 6.1 회원가입 테스트

1. 정상 회원가입: 유효한 이메일, 비밀번호, 이름
2. 이메일 중복: 이미 존재하는 이메일로 회원가입 시도
3. 이메일 형식 오류: 잘못된 이메일 형식
4. 비밀번호 길이 부족: 8자 미만 비밀번호
5. 이름 길이 부족: 2자 미만 이름

### 6.2 로그인 테스트

1. 정상 로그인: 유효한 이메일과 비밀번호
2. 이메일 없음: 존재하지 않는 이메일
3. 비밀번호 불일치: 잘못된 비밀번호
4. 이메일 형식 오류: 잘못된 이메일 형식
5. 비밀번호 길이 부족: 8자 미만 비밀번호

---

**작성일**: 2025-01-27  
**버전**: 1.0  
**작성자**: Backend Development Team

