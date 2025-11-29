# JWT 토큰 검증 미들웨어 구현

- **Type**: Functional
- **Key**: BE-AUTH-002
- **REQ / Epic**: REQ-FUNC-037
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-001

## 📌 Description

Spring Security를 사용하여 JWT 토큰 검증 필터를 구현합니다. 모든 보호된 엔드포인트에 대해 토큰 검증을 수행하고, 유효하지 않은 토큰에 대해서는 401 Unauthorized를 반환합니다.

## ✅ Acceptance Criteria

### 필터 구현
- [ ] `JwtAuthenticationFilter` 클래스 생성 (OncePerRequestFilter 확장)
- [ ] Authorization 헤더에서 Bearer 토큰 추출 로직 구현
- [ ] JWT 토큰 파싱 및 Claims 추출
- [ ] 토큰 유효성 검증 (서명 검증)
- [ ] 토큰 만료 확인 로직 구현
- [ ] 사용자 정보 추출 및 SecurityContext 설정

### Spring Security 설정
- [ ] `SecurityConfig` 클래스 확장 (SecurityFilterChain Bean)
- [ ] `JwtAuthenticationFilter` 필터 체인에 등록
- [ ] `JwtAuthenticationEntryPoint` 구현 (인증 실패 처리)
- [ ] Public endpoints 설정 (login, swagger 등)
- [ ] CORS 설정

### 에러 응답
- [ ] 토큰 없음 시 401 반환 (AUTH_001)
- [ ] 토큰 만료 시 401 반환 (AUTH_005)
- [ ] 토큰 무효 시 401 반환 (AUTH_006)

### 성능 및 테스트
- [ ] 인증 검증 시간 100ms 이내
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

---

## 🧩 Technical Notes

### 구현 클래스 목록

| 클래스 | 패키지 | 설명 |
|--------|--------|------|
| `JwtAuthenticationFilter` | `security` | JWT 검증 필터 (OncePerRequestFilter 확장) |
| `JwtTokenProvider` | `security` | 토큰 검증/파싱 메서드 추가 (BE-AUTH-001에서 생성) |
| `SecurityConfig` | `config` | Spring Security 설정 확장 |
| `JwtAuthenticationEntryPoint` | `security` | 401 응답 처리 핸들러 |

### 필수 의존성 (build.gradle)

```gradle
dependencies {
    // Spring Boot Starters
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    
    // JWT (jjwt 0.12.x - Spring Boot 4.0 호환)
    implementation 'io.jsonwebtoken:jjwt-api:0.12.6'
    runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.12.6'
    runtimeOnly 'io.jsonwebtoken:jjwt-jackson:0.12.6'
    
    // Database
    runtimeOnly 'com.mysql:mysql-connector-j'
    
    // Lombok
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    
    // Test
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.springframework.security:spring-security-test'
}
```

### Spring Boot 4.0 / Security 7.x 고려사항

| 변경 사항 | Spring Boot 3.x | Spring Boot 4.0 |
|----------|-----------------|-----------------|
| Security Config | `@EnableWebSecurity` | 동일 (유지) |
| Filter Chain | `SecurityFilterChain` Bean | 동일 (유지) |
| URL Matcher | `antMatchers()` | `requestMatchers()` |
| Authorization | `authorizeRequests()` | `authorizeHttpRequests()` |
| DSL Style | 메서드 체인 | Lambda DSL 권장 |

---

## 📋 API 명세서

### 1. 인증 헤더 형식

| 항목 | 내용 |
|------|------|
| **Header Name** | `Authorization` |
| **Header Value** | `Bearer {JWT_TOKEN}` |
| **토큰 위치** | "Bearer " 접두사 이후 (7번째 문자부터) |

**요청 헤더 예시:**
```http
GET /api/v1/students HTTP/1.1
Host: api.reacademix.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

### 2. Public Endpoints (인증 제외)

| HTTP Method | URI Pattern | 설명 |
|-------------|-------------|------|
| `POST` | `/api/v1/auth/login` | 로그인 |
| `POST` | `/api/v1/auth/signup` | 회원가입 (향후) |
| `GET` | `/health` | 헬스 체크 |
| `GET` | `/actuator/**` | Actuator 엔드포인트 |
| `GET` | `/swagger-ui/**` | Swagger UI |
| `GET` | `/v3/api-docs/**` | OpenAPI 스펙 |
| `GET` | `/swagger-resources/**` | Swagger 리소스 |

### 3. 에러 응답

#### 3.1 에러 코드 정의

| HTTP Status | 에러 코드 | 에러 메시지 | 발생 조건 |
|-------------|----------|------------|----------|
| `401 Unauthorized` | `AUTH_001` | "인증 토큰이 필요합니다." | Authorization 헤더가 없거나 Bearer 형식이 아님 |
| `401 Unauthorized` | `AUTH_005` | "토큰이 만료되었습니다." | JWT 토큰의 exp claim이 현재 시간보다 이전 |
| `401 Unauthorized` | `AUTH_006` | "유효하지 않은 토큰입니다." | JWT 서명 검증 실패, 파싱 실패, 또는 변조된 토큰 |
| `401 Unauthorized` | `AUTH_007` | "사용자 정보를 찾을 수 없습니다." | 토큰의 userId로 사용자 조회 실패 |

#### 3.2 에러 응답 형식

**에러 응답 예시 (토큰 없음):**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_001",
    "message": "인증 토큰이 필요합니다.",
    "details": null
  },
  "timestamp": "2025-12-12T10:30:00Z"
}
```

**에러 응답 예시 (토큰 만료):**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_005",
    "message": "토큰이 만료되었습니다.",
    "details": {
      "expiredAt": "2025-12-11T10:30:00Z"
    }
  },
  "timestamp": "2025-12-12T10:30:00Z"
}
```

**에러 응답 예시 (유효하지 않은 토큰):**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_006",
    "message": "유효하지 않은 토큰입니다.",
    "details": null
  },
  "timestamp": "2025-12-12T10:30:00Z"
}
```

### 4. JWT 토큰 구조

#### 4.1 토큰 Claims (BE-AUTH-001에서 생성)

| Claim | 타입 | 설명 |
|-------|------|------|
| `sub` | String | 사용자 ID (userId) |
| `email` | String | 사용자 이메일 |
| `role` | String | 사용자 역할 (ADMIN, MANAGER, STAFF) |
| `iat` | Long | 토큰 발급 시간 (Unix timestamp) |
| `exp` | Long | 토큰 만료 시간 (Unix timestamp, 발급 후 24시간) |

#### 4.2 토큰 검증 순서

```
1. Authorization 헤더 존재 확인
   ↓ (없으면 AUTH_001)
2. "Bearer " 접두사 확인
   ↓ (없으면 AUTH_001)
3. JWT 토큰 파싱 (서명 검증)
   ↓ (실패하면 AUTH_006)
4. exp claim 확인 (만료 검증)
   ↓ (만료되면 AUTH_005)
5. sub claim에서 userId 추출
   ↓
6. UserRepository에서 사용자 조회
   ↓ (없으면 AUTH_007)
7. SecurityContext에 Authentication 설정
   ↓
8. 다음 필터로 진행
```

### 5. CORS 설정

| 항목 | 개발 환경 | 운영 환경 |
|------|----------|----------|
| **Allowed Origins** | `http://localhost:3000`, `http://localhost:5173` | 도메인 설정 필요 |
| **Allowed Methods** | `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS` | 동일 |
| **Allowed Headers** | `Authorization`, `Content-Type`, `X-Requested-With` | 동일 |
| **Exposed Headers** | `Authorization` | 동일 |
| **Allow Credentials** | `true` | `true` |
| **Max Age** | `3600` (1시간) | `3600` |

### 6. Logic Steps (필터 처리 순서)

| 단계 | 처리 내용 | 구현 위치 | 비고 |
|------|----------|----------|------|
| **1. 헤더 추출** | `Authorization` 헤더에서 토큰 추출 | `JwtAuthenticationFilter` | "Bearer " 접두사 제거 |
| **2. Public Path 확인** | 인증 제외 경로인지 확인 | `SecurityConfig` | 제외 경로면 필터 통과 |
| **3. 토큰 검증** | JWT 서명 및 유효성 검증 | `JwtTokenProvider` | jjwt 라이브러리 사용 |
| **4. 만료 확인** | exp claim과 현재 시간 비교 | `JwtTokenProvider` | 만료 시 AUTH_005 |
| **5. 사용자 조회** | userId로 사용자 정보 조회 | `UserRepository` | 없으면 AUTH_007 |
| **6. Authentication 생성** | UsernamePasswordAuthenticationToken 생성 | `JwtAuthenticationFilter` | authorities 포함 |
| **7. SecurityContext 설정** | SecurityContextHolder에 Authentication 저장 | `JwtAuthenticationFilter` | 요청 스코프 유지 |
| **8. 필터 체인 진행** | 다음 필터 또는 컨트롤러로 전달 | `JwtAuthenticationFilter` | `filterChain.doFilter()` |

### 7. Difficulty (예상 구현 난이도)

| 항목 | 난이도 | 이유 |
|------|--------|------|
| **전체 난이도** | **중 (Medium)** | Spring Security 설정 이해 필요 |
| **토큰 추출** | 하 (Low) | 단순 문자열 파싱 |
| **토큰 검증** | 중 (Medium) | jjwt 라이브러리 사용법 숙지 필요 |
| **Security 설정** | 중 (Medium) | Spring Security 7.x 변경사항 적용 |
| **예외 처리** | 중 (Medium) | 다양한 예외 케이스 처리 |
| **테스트 작성** | 중 (Medium) | MockMvc + Security 테스트 설정 |

---

## 📊 1. ERD (Entity Relationship Diagram)

**JWT 토큰 검증에 사용되는 데이터 구조** (데이터베이스 관점)

```mermaid
erDiagram
    User ||--o{ UserLoginHistory : "has many (optional)"
    
    User {
        BIGINT id PK "AUTO_INCREMENT, NOT NULL"
        VARCHAR email UK "UNIQUE, NOT NULL, 최대 255자, 인덱스"
        VARCHAR password "NOT NULL, bcrypt 해시, 최대 255자"
        VARCHAR name "NOT NULL, 최대 100자"
        VARCHAR role "NOT NULL, DEFAULT 'ADMIN', ENUM('ADMIN', 'MANAGER', 'STAFF')"
        VARCHAR status "NOT NULL, DEFAULT 'ACTIVE', ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED')"
        TIMESTAMP created_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP updated_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE"
    }
    
    UserLoginHistory {
        BIGINT id PK "AUTO_INCREMENT, NOT NULL"
        BIGINT user_id FK "NOT NULL, 인덱스"
        VARCHAR ip_address "NULL, 최대 45자 (IPv6 지원)"
        VARCHAR user_agent "NULL, 최대 500자"
        VARCHAR login_status "NOT NULL, ENUM('SUCCESS', 'FAILED')"
        VARCHAR failure_reason "NULL, ENUM('INVALID_EMAIL', 'INVALID_PASSWORD', 'TOKEN_EXPIRED')"
        TIMESTAMP login_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP, 인덱스"
    }
```

### 테이블 상세 설계

#### users 테이블 (JWT 검증 시 조회)

| 컬럼명 | 타입 | 제약조건 | JWT 검증 시 사용 |
|--------|------|----------|-----------------|
| `id` | BIGINT | PK, AUTO_INCREMENT, NOT NULL | ✅ sub claim과 매핑 |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | ✅ email claim 검증 |
| `password` | VARCHAR(255) | NOT NULL | ❌ 검증 시 미사용 |
| `name` | VARCHAR(100) | NOT NULL | ✅ 사용자 정보 제공 |
| `role` | VARCHAR(20) | NOT NULL, DEFAULT 'ADMIN', INDEX | ✅ role claim 검증, authorities 생성 |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'ACTIVE', INDEX | ✅ ACTIVE 상태 확인 |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | ❌ 검증 시 미사용 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | ❌ 검증 시 미사용 |

**인덱스:**
- PRIMARY KEY: `id` (JWT sub claim 조회)
- UNIQUE INDEX: `email` (이메일 중복 방지)
- INDEX: `status` (활성 사용자 필터링)
- INDEX: `role` (역할별 권한 조회)

**JWT 검증 시 쿼리:**
```sql
SELECT id, email, name, role, status 
FROM users 
WHERE id = ? AND status = 'ACTIVE'
```

---

## 🏛️ 2. CLD (Class/Component Logic Diagram)

**필터가 어떻게 동작하는가?** (백엔드 서버 관점)

```mermaid
graph TB
    subgraph "HTTP Request"
        REQ[HTTP Request with Authorization Header]
    end
    
    subgraph "Security Filter Chain"
        JAF[JwtAuthenticationFilter]
        JAF --> |"1. 헤더 추출<br/>2. Bearer 토큰 파싱"| JTP
        JAF --> |"6. Authentication 설정"| SC[SecurityContext]
    end
    
    subgraph "Security Components"
        JTP[JwtTokenProvider]
        JTP --> |"3. 토큰 검증<br/>4. Claims 추출"| CLAIMS[JWT Claims]
        JTP --> |"검증 실패"| JAEP[JwtAuthenticationEntryPoint]
    end
    
    subgraph "Data Layer"
        UR[UserRepository]
        UR --> |"5. 사용자 조회"| USER[User Entity]
        UR --> |"Optional〈User〉"| JAF
    end
    
    subgraph "Controller Layer"
        CTRL[Protected Controller]
        CTRL --> |"@PreAuthorize<br/>권한 확인"| SC
    end
    
    subgraph "Error Response"
        JAEP --> |"401 Unauthorized"| ERR[ErrorResponse JSON]
    end
    
    REQ --> JAF
    SC --> CTRL
    
    style JAF fill:#e1f5ff
    style JTP fill:#fff4e1
    style SC fill:#e8f5e9
    style JAEP fill:#ffebee
```

### 컴포넌트별 책임

| 컴포넌트 | 책임 | 주요 메서드 |
|----------|------|-----------|
| `JwtAuthenticationFilter` | 요청 인터셉트, 토큰 추출, SecurityContext 설정 | `doFilterInternal()` |
| `JwtTokenProvider` | 토큰 검증, Claims 추출 | `validateToken()`, `getUserIdFromToken()`, `getClaimsFromToken()` |
| `JwtAuthenticationEntryPoint` | 인증 실패 시 401 응답 생성 | `commence()` |
| `SecurityConfig` | 필터 체인 설정, 경로별 권한 설정 | `securityFilterChain()` |

---

## 🔄 3. Sequence Diagram (시퀀스 다이어그램)

### 3.1 JWT 토큰 검증 성공 흐름

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Provider as JwtTokenProvider
    participant Repo as UserRepository
    participant DB as MySQL Database
    participant Context as SecurityContext
    participant Controller as Protected Controller

    Client->>+Filter: HTTP Request (Authorization: Bearer token)
    
    Note over Filter: 1. Authorization 헤더 추출
    Filter->>Filter: extractToken(request)
    
    Note over Filter: 2. Bearer 접두사 제거
    Filter->>+Provider: validateToken(token)
    
    Note over Provider: 3. JWT 서명 검증
    Provider->>Provider: Jwts.parser().verifyWith(secretKey)
    
    Note over Provider: 4. 만료 시간 확인
    Provider->>Provider: Check exp claim
    Provider-->>-Filter: true (유효)
    
    Filter->>+Provider: getUserIdFromToken(token)
    Provider-->>-Filter: userId (Long)
    
    Note over Filter: 5. 사용자 조회
    Filter->>+Repo: findById(userId)
    Repo->>+DB: SELECT * FROM users WHERE id = ?
    DB-->>-Repo: User record
    Repo-->>-Filter: Optional<User>
    
    Note over Filter: 6. Authentication 객체 생성
    Filter->>Filter: UsernamePasswordAuthenticationToken 생성
    
    Note over Filter: 7. SecurityContext 설정
    Filter->>Context: setAuthentication(authentication)
    
    Note over Filter: 8. 필터 체인 진행
    Filter->>+Controller: filterChain.doFilter()
    
    Controller-->>-Filter: Response
    Filter-->>-Client: HTTP Response (200 OK)
```

### 3.2 JWT 토큰 검증 실패 흐름 (토큰 만료)

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Provider as JwtTokenProvider
    participant EntryPoint as JwtAuthenticationEntryPoint
    participant ObjectMapper as ObjectMapper

    Client->>+Filter: HTTP Request (Authorization: Bearer expired_token)
    
    Note over Filter: 1. Authorization 헤더 추출
    Filter->>Filter: extractToken(request)
    
    Filter->>+Provider: validateToken(token)
    
    Note over Provider: JWT 파싱 시도
    Provider->>Provider: Jwts.parser().parseSignedClaims()
    
    Note over Provider: ExpiredJwtException 발생!
    Provider->>Provider: catch ExpiredJwtException
    Provider->>Provider: log.error("JWT token is expired")
    Provider-->>-Filter: false (무효)
    
    Note over Filter: 인증 정보 없이 필터 체인 진행
    Filter->>Filter: SecurityContext 비어있음
    
    Note over Filter: 보호된 엔드포인트 접근 시
    Filter->>+EntryPoint: commence(request, response, exception)
    
    EntryPoint->>EntryPoint: ErrorResponse 생성 (AUTH_005)
    EntryPoint->>+ObjectMapper: writeValue(response, errorResponse)
    ObjectMapper-->>-EntryPoint: JSON 직렬화 완료
    
    EntryPoint->>EntryPoint: response.setStatus(401)
    EntryPoint-->>-Filter: 응답 완료
    
    Filter-->>-Client: HTTP Response (401 Unauthorized)
    
    Note over Client: {<br/>"success": false,<br/>"error": { "code": "AUTH_005", "message": "토큰이 만료되었습니다." }<br/>}
```

### 3.3 JWT 토큰 없음 흐름

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant EntryPoint as JwtAuthenticationEntryPoint
    participant Controller as Protected Controller

    Client->>+Filter: HTTP Request (Authorization 헤더 없음)
    
    Note over Filter: 1. Authorization 헤더 추출 시도
    Filter->>Filter: extractToken(request)
    Filter->>Filter: return null (헤더 없음)
    
    Note over Filter: 토큰이 없으므로 검증 스킵
    Filter->>Filter: if (!StringUtils.hasText(token)) skip
    
    Note over Filter: SecurityContext 비어있는 상태로 진행
    Filter->>+Controller: filterChain.doFilter()
    
    Note over Controller: @PreAuthorize 또는 인증 필요 체크
    Controller->>Controller: SecurityContext.getAuthentication() == null
    
    Controller-->>-Filter: AuthenticationException 발생
    
    Filter->>+EntryPoint: commence(request, response, exception)
    
    EntryPoint->>EntryPoint: ErrorResponse 생성 (AUTH_001)
    EntryPoint->>EntryPoint: response.setStatus(401)
    EntryPoint-->>-Filter: 응답 완료
    
    Filter-->>-Client: HTTP Response (401 Unauthorized)
    
    Note over Client: {<br/>"success": false,<br/>"error": { "code": "AUTH_001", "message": "인증 토큰이 필요합니다." }<br/>}
```

### 3.4 사용자 조회 실패 흐름

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Provider as JwtTokenProvider
    participant Repo as UserRepository
    participant DB as MySQL Database
    participant EntryPoint as JwtAuthenticationEntryPoint

    Client->>+Filter: HTTP Request (Authorization: Bearer valid_token)
    
    Filter->>Filter: extractToken(request)
    
    Filter->>+Provider: validateToken(token)
    Provider-->>-Filter: true (유효)
    
    Filter->>+Provider: getUserIdFromToken(token)
    Provider-->>-Filter: userId = 999 (존재하지 않는 ID)
    
    Note over Filter: 사용자 조회
    Filter->>+Repo: findById(999)
    Repo->>+DB: SELECT * FROM users WHERE id = 999
    DB-->>-Repo: Empty result
    Repo-->>-Filter: Optional.empty()
    
    Note over Filter: 사용자 없음 - Authentication 생성 안 함
    Filter->>Filter: if (user == null) skip authentication
    
    Note over Filter: SecurityContext 비어있는 상태로 진행
    Filter->>Filter: filterChain.doFilter()
    
    Note over Filter: 보호된 엔드포인트 접근 시 인증 실패
    Filter->>+EntryPoint: commence(request, response, exception)
    
    EntryPoint->>EntryPoint: ErrorResponse 생성 (AUTH_007)
    EntryPoint-->>-Filter: 응답 완료
    
    Filter-->>-Client: HTTP Response (401 Unauthorized)
    
    Note over Client: {<br/>"success": false,<br/>"error": { "code": "AUTH_007", "message": "사용자 정보를 찾을 수 없습니다." }<br/>}
```

---

## 💻 4. ORM 예제 코드

### 4.1 JPA Entity (User.java)

```java
package com.reacademix.reacademix_backend.domain.user;

import com.reacademix.reacademix_backend.common.BaseTimeEntity;
import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * User 엔티티
 * 사용자 기본 정보를 저장하는 JPA 엔티티
 * JWT 토큰 검증 시 userId로 조회하여 인증 정보 생성
 * 
 * @author Backend Team
 * @version 1.0
 */
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_users_email", columnList = "email"),
    @Index(name = "idx_users_status", columnList = "status"),
    @Index(name = "idx_users_role", columnList = "role")
})
@Getter
@NoArgsConstructor
public class User extends BaseTimeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(nullable = false, length = 255)
    private String password;  // bcrypt 해시

    @Column(nullable = false, length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private UserRole role = UserRole.ADMIN;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private UserStatus status = UserStatus.ACTIVE;

    @Builder
    public User(String email, String password, String name, UserRole role, UserStatus status) {
        this.email = email != null ? email.toLowerCase() : null;
        this.password = password;
        this.name = name;
        this.role = role != null ? role : UserRole.ADMIN;
        this.status = status != null ? status : UserStatus.ACTIVE;
    }

    /**
     * 사용자 계정 활성화 상태 확인
     * JWT 토큰 검증 시 사용
     * 
     * @return 활성화 여부
     */
    public boolean isActive() {
        return this.status == UserStatus.ACTIVE;
    }
}
```

### 4.2 Enum 클래스

```java
package com.reacademix.reacademix_backend.domain.user;

/**
 * 사용자 역할 Enum
 * JWT claim의 role과 매핑되어 Spring Security authorities 생성에 사용
 */
public enum UserRole {
    ADMIN,      // 관리자 (MVP 기본값)
    MANAGER,    // 관리자 (확장)
    STAFF       // 직원 (확장)
}
```

```java
package com.reacademix.reacademix_backend.domain.user;

/**
 * 사용자 상태 Enum
 * JWT 토큰 검증 시 ACTIVE 상태만 인증 허용
 */
public enum UserStatus {
    ACTIVE,     // 정상 사용 가능 (인증 허용)
    INACTIVE,   // 비활성화 (인증 거부)
    SUSPENDED   // 일시 정지 (인증 거부)
}
```

### 4.3 Repository 인터페이스 (UserRepository.java)

```java
package com.reacademix.reacademix_backend.repository;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * User 엔티티를 위한 Repository 인터페이스
 * JWT 토큰 검증 시 사용자 조회에 사용
 * 
 * @author Backend Team
 * @version 1.0
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * 이메일로 사용자 조회 (로그인 시 사용)
     * 
     * @param email 사용자 이메일
     * @return Optional<User> 사용자 정보
     * 
     * SQL: SELECT * FROM users WHERE email = ? LIMIT 1
     */
    Optional<User> findByEmail(String email);

    /**
     * ID와 상태로 사용자 조회 (JWT 검증 시 사용)
     * 활성화된 사용자만 인증 허용
     * 
     * @param id 사용자 ID (JWT sub claim)
     * @param status 사용자 상태 (ACTIVE)
     * @return Optional<User> 사용자 정보
     * 
     * SQL: SELECT * FROM users WHERE id = ? AND status = ? LIMIT 1
     */
    Optional<User> findByIdAndStatus(Long id, UserStatus status);

    /**
     * ID로 활성 사용자 조회 (JWT 검증 최적화)
     * 
     * @param id 사용자 ID (JWT sub claim)
     * @return Optional<User> 활성 사용자 정보
     * 
     * SQL: SELECT * FROM users WHERE id = ? AND status = 'ACTIVE' LIMIT 1
     */
    @Query("SELECT u FROM User u WHERE u.id = :id AND u.status = 'ACTIVE'")
    Optional<User> findActiveUserById(@Param("id") Long id);

    /**
     * 이메일 존재 여부 확인
     * 
     * @param email 사용자 이메일
     * @return boolean 존재 여부
     */
    boolean existsByEmail(String email);
}
```

### 4.4 JwtAuthenticationFilter.java

```java
package com.reacademix.reacademix_backend.security;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import com.reacademix.reacademix_backend.repository.UserRepository;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

/**
 * JWT 토큰 인증 필터
 * 모든 요청에서 Authorization 헤더의 JWT 토큰을 검증하고 SecurityContext에 인증 정보 설정
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtTokenProvider jwtTokenProvider;
    private final UserRepository userRepository;

    private static final String AUTHORIZATION_HEADER = "Authorization";
    private static final String BEARER_PREFIX = "Bearer ";

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {
        
        try {
            // 1. Authorization 헤더에서 JWT 토큰 추출
            String token = extractToken(request);
            
            // 2. 토큰이 존재하고 유효한 경우
            if (StringUtils.hasText(token) && jwtTokenProvider.validateToken(token)) {
                // 3. 토큰에서 사용자 ID 추출
                Long userId = jwtTokenProvider.getUserIdFromToken(token);
                
                // 4. 활성 사용자 조회 (Repository Layer 호출)
                User user = userRepository.findByIdAndStatus(userId, UserStatus.ACTIVE)
                    .orElse(null);
                
                if (user != null) {
                    // 5. Authentication 객체 생성
                    List<SimpleGrantedAuthority> authorities = List.of(
                        new SimpleGrantedAuthority("ROLE_" + user.getRole().name())
                    );
                    
                    UsernamePasswordAuthenticationToken authentication = 
                        new UsernamePasswordAuthenticationToken(user, null, authorities);
                    authentication.setDetails(
                        new WebAuthenticationDetailsSource().buildDetails(request));
                    
                    // 6. SecurityContext에 Authentication 설정
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    
                    log.debug("인증 성공: userId={}, email={}, role={}", 
                        userId, user.getEmail(), user.getRole());
                } else {
                    log.warn("인증 실패: 사용자 없음 또는 비활성 - userId={}", userId);
                }
            }
        } catch (Exception e) {
            log.error("JWT 인증 처리 중 오류 발생: {}", e.getMessage());
            // 예외가 발생해도 필터 체인은 계속 진행 (인증 없이)
            // EntryPoint에서 401 처리
        }
        
        // 7. 다음 필터로 진행
        filterChain.doFilter(request, response);
    }

    /**
     * Authorization 헤더에서 Bearer 토큰 추출
     * 
     * @param request HTTP 요청
     * @return JWT 토큰 문자열 (없으면 null)
     */
    private String extractToken(HttpServletRequest request) {
        String bearerToken = request.getHeader(AUTHORIZATION_HEADER);
        
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith(BEARER_PREFIX)) {
            return bearerToken.substring(BEARER_PREFIX.length());
        }
        
        return null;
    }
}
```

### 4.5 JwtTokenProvider.java (검증 메서드 추가)

```java
package com.reacademix.reacademix_backend.security;

import com.reacademix.reacademix_backend.domain.user.User;
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import io.jsonwebtoken.security.SignatureException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT 토큰 생성 및 검증을 담당하는 Provider 클래스
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@Component
public class JwtTokenProvider {

    private final SecretKey secretKey;
    private final long expirationTime;

    public JwtTokenProvider(
            @Value("${jwt.secret}") String secret,
            @Value("${jwt.expiration:86400000}") long expirationTime) {
        // 최소 256비트(32바이트) 이상의 키 필요
        this.secretKey = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.expirationTime = expirationTime;
    }

    /**
     * JWT 토큰 생성 (BE-AUTH-001에서 호출)
     * 
     * @param user 사용자 엔티티
     * @return 생성된 JWT 토큰
     */
    public String generateToken(User user) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expirationTime);

        return Jwts.builder()
            .subject(String.valueOf(user.getId()))
            .claim("email", user.getEmail())
            .claim("role", user.getRole().name())
            .issuedAt(now)
            .expiration(expiryDate)
            .signWith(secretKey, Jwts.SIG.HS256)
            .compact();
    }

    /**
     * JWT 토큰 유효성 검증
     * 
     * @param token JWT 토큰
     * @return 유효 여부 (true: 유효, false: 무효)
     */
    public boolean validateToken(String token) {
        try {
            Jwts.parser()
                .verifyWith(secretKey)
                .build()
                .parseSignedClaims(token);
            return true;
        } catch (SignatureException e) {
            log.error("Invalid JWT signature: {}", e.getMessage());
        } catch (MalformedJwtException e) {
            log.error("Invalid JWT token: {}", e.getMessage());
        } catch (ExpiredJwtException e) {
            log.error("JWT token is expired: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            log.error("JWT token is unsupported: {}", e.getMessage());
        } catch (IllegalArgumentException e) {
            log.error("JWT claims string is empty: {}", e.getMessage());
        }
        return false;
    }

    /**
     * 토큰에서 사용자 ID 추출
     * 
     * @param token JWT 토큰
     * @return 사용자 ID
     */
    public Long getUserIdFromToken(String token) {
        Claims claims = getClaimsFromToken(token);
        return Long.parseLong(claims.getSubject());
    }

    /**
     * 토큰에서 이메일 추출
     * 
     * @param token JWT 토큰
     * @return 사용자 이메일
     */
    public String getEmailFromToken(String token) {
        Claims claims = getClaimsFromToken(token);
        return claims.get("email", String.class);
    }

    /**
     * 토큰에서 역할 추출
     * 
     * @param token JWT 토큰
     * @return 사용자 역할
     */
    public String getRoleFromToken(String token) {
        Claims claims = getClaimsFromToken(token);
        return claims.get("role", String.class);
    }

    /**
     * 토큰에서 Claims 추출
     * 
     * @param token JWT 토큰
     * @return Claims 객체
     */
    public Claims getClaimsFromToken(String token) {
        return Jwts.parser()
            .verifyWith(secretKey)
            .build()
            .parseSignedClaims(token)
            .getPayload();
    }

    /**
     * 토큰 만료 시간 반환 (초 단위)
     * 
     * @return 만료 시간 (초)
     */
    public long getExpirationInSeconds() {
        return expirationTime / 1000;
    }
}
```

### 4.6 JwtAuthenticationEntryPoint.java

```java
package com.reacademix.reacademix_backend.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.reacademix.reacademix_backend.dto.response.ErrorResponse;
import com.reacademix.reacademix_backend.exception.ErrorCode;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.time.LocalDateTime;

/**
 * JWT 인증 실패 시 401 Unauthorized 응답을 처리하는 EntryPoint
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint {

    private final ObjectMapper objectMapper;

    @Override
    public void commence(
            HttpServletRequest request,
            HttpServletResponse response,
            AuthenticationException authException) throws IOException, ServletException {
        
        log.error("Unauthorized error: {} - URI: {}", 
            authException.getMessage(), request.getRequestURI());
        
        // 에러 코드 결정 (request attribute에서 가져오거나 기본값 사용)
        ErrorCode errorCode = (ErrorCode) request.getAttribute("errorCode");
        if (errorCode == null) {
            errorCode = ErrorCode.AUTH_001;
        }
        
        // 에러 응답 생성
        ErrorResponse errorResponse = ErrorResponse.builder()
            .success(false)
            .error(ErrorResponse.ErrorDetail.builder()
                .code(errorCode.getCode())
                .message(errorCode.getMessage())
                .details(null)
                .build())
            .timestamp(LocalDateTime.now())
            .build();
        
        // HTTP 응답 설정
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        
        // JSON 응답 출력
        objectMapper.writeValue(response.getOutputStream(), errorResponse);
    }
}
```

### 4.7 SecurityConfig.java (확장)

```java
package com.reacademix.reacademix_backend.config;

import com.reacademix.reacademix_backend.security.JwtAuthenticationEntryPoint;
import com.reacademix.reacademix_backend.security.JwtAuthenticationFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

/**
 * Spring Security 설정
 * JWT 기반 인증 필터 체인 구성
 * 
 * @author Backend Team
 * @version 1.0
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;
    private final JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint;

    /**
     * Public endpoints - 인증 없이 접근 가능한 경로
     */
    private static final String[] PUBLIC_ENDPOINTS = {
        "/api/v1/auth/login",
        "/api/v1/auth/signup",
        "/health",
        "/actuator/**",
        "/swagger-ui/**",
        "/swagger-ui.html",
        "/v3/api-docs/**",
        "/swagger-resources/**",
        "/webjars/**"
    };

    /**
     * PasswordEncoder Bean 등록
     * bcrypt 알고리즘 사용 (salt rounds: 10)
     * 
     * @return PasswordEncoder BCryptPasswordEncoder 인스턴스
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);
    }

    /**
     * Security Filter Chain 설정
     * Spring Security 7.x (Spring Boot 4.0) 호환
     * 
     * @param http HttpSecurity 객체
     * @return SecurityFilterChain
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // CSRF 비활성화 (JWT 사용으로 불필요)
            .csrf(AbstractHttpConfigurer::disable)
            
            // CORS 설정
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            
            // 세션 관리 - STATELESS (JWT 사용)
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            
            // 예외 처리 - 인증 실패 시 EntryPoint 호출
            .exceptionHandling(exception -> 
                exception.authenticationEntryPoint(jwtAuthenticationEntryPoint))
            
            // 경로별 권한 설정
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(PUBLIC_ENDPOINTS).permitAll()
                .anyRequest().authenticated())
            
            // JWT 필터 추가 (UsernamePasswordAuthenticationFilter 이전)
            .addFilterBefore(jwtAuthenticationFilter, 
                UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }

    /**
     * CORS 설정
     * 
     * @return CorsConfigurationSource
     */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        
        // 허용 Origin (개발 환경)
        configuration.setAllowedOrigins(Arrays.asList(
            "http://localhost:3000",
            "http://localhost:5173"
        ));
        
        // 허용 HTTP Methods
        configuration.setAllowedMethods(Arrays.asList(
            "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"
        ));
        
        // 허용 Headers
        configuration.setAllowedHeaders(Arrays.asList(
            "Authorization",
            "Content-Type",
            "X-Requested-With"
        ));
        
        // 노출 Headers
        configuration.setExposedHeaders(List.of("Authorization"));
        
        // 자격 증명 허용
        configuration.setAllowCredentials(true);
        
        // Preflight 캐시 시간 (1시간)
        configuration.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        
        return source;
    }
}
```

### 4.8 ErrorResponse.java

```java
package com.reacademix.reacademix_backend.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 에러 응답 DTO
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {

    private boolean success;
    private ErrorDetail error;
    private LocalDateTime timestamp;

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ErrorDetail {
        private String code;
        private String message;
        private Object details;
    }
}
```

### 4.9 ErrorCode.java (확장)

```java
package com.reacademix.reacademix_backend.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

/**
 * 에러 코드 Enum
 * HTTP 상태 코드와 함께 에러 정보 관리
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    
    // 인증 관련 에러 (AUTH_XXX)
    AUTH_001("AUTH_001", "인증 토큰이 필요합니다.", HttpStatus.UNAUTHORIZED),
    AUTH_002("AUTH_002", "이메일 또는 비밀번호가 올바르지 않습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_003("AUTH_003", "이메일 또는 비밀번호가 올바르지 않습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_004("AUTH_004", "계정이 비활성화되었습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_005("AUTH_005", "토큰이 만료되었습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_006("AUTH_006", "유효하지 않은 토큰입니다.", HttpStatus.UNAUTHORIZED),
    AUTH_007("AUTH_007", "사용자 정보를 찾을 수 없습니다.", HttpStatus.UNAUTHORIZED),
    
    // 검증 관련 에러 (VALIDATION_XXX)
    VALIDATION_001("VALIDATION_001", "입력 데이터 검증에 실패했습니다.", HttpStatus.BAD_REQUEST),
    VALIDATION_002("VALIDATION_002", "올바른 이메일 형식이 아닙니다.", HttpStatus.BAD_REQUEST),
    VALIDATION_003("VALIDATION_003", "비밀번호는 최소 8자 이상이어야 합니다.", HttpStatus.BAD_REQUEST),
    
    // 시스템 에러 (SYSTEM_XXX)
    SYSTEM_001("SYSTEM_001", "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요.", HttpStatus.INTERNAL_SERVER_ERROR),
    SYSTEM_003("SYSTEM_003", "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요.", HttpStatus.INTERNAL_SERVER_ERROR);

    private final String code;
    private final String message;
    private final HttpStatus httpStatus;
}
```

### 4.10 BaseTimeEntity.java (공통)

```java
package com.reacademix.reacademix_backend.common;

import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.MappedSuperclass;
import lombok.Getter;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

/**
 * JPA Auditing을 위한 기본 시간 엔티티
 * 모든 엔티티에서 상속받아 createdAt, updatedAt 자동 관리
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseTimeEntity {

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
}
```

### 4.11 application.properties (JWT 설정)

```properties
spring.application.name=reacademix-backend

# JWT Configuration
jwt.secret=your-256-bit-secret-key-here-must-be-at-least-32-characters-long
jwt.expiration=86400000

# Database Configuration (MySQL)
spring.datasource.url=jdbc:mysql://localhost:3306/reacademix?useSSL=false&serverTimezone=Asia/Seoul&characterEncoding=UTF-8
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA Configuration
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
```

---

## 🧪 5. 테스트 코드

### 5.1 JwtTokenProviderTest.java

```java
package com.reacademix.reacademix_backend.security;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserRole;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * JwtTokenProvider 단위 테스트
 */
class JwtTokenProviderTest {

    private JwtTokenProvider jwtTokenProvider;
    private User testUser;

    @BeforeEach
    void setUp() {
        // 32바이트 이상의 시크릿 키
        String secret = "test-secret-key-must-be-at-least-32-characters";
        long expiration = 86400000L; // 24시간
        
        jwtTokenProvider = new JwtTokenProvider(secret, expiration);
        
        testUser = User.builder()
            .email("test@academy.com")
            .password("encodedPassword")
            .name("테스트 사용자")
            .role(UserRole.ADMIN)
            .status(UserStatus.ACTIVE)
            .build();
        
        // ID 설정 (리플렉션 사용)
        setUserId(testUser, 1L);
    }

    @Test
    @DisplayName("토큰 생성 성공")
    void generateToken_Success() {
        // when
        String token = jwtTokenProvider.generateToken(testUser);
        
        // then
        assertThat(token).isNotNull();
        assertThat(token.split("\\.")).hasSize(3); // Header.Payload.Signature
    }

    @Test
    @DisplayName("토큰 검증 성공")
    void validateToken_Success() {
        // given
        String token = jwtTokenProvider.generateToken(testUser);
        
        // when
        boolean isValid = jwtTokenProvider.validateToken(token);
        
        // then
        assertThat(isValid).isTrue();
    }

    @Test
    @DisplayName("잘못된 토큰 검증 실패")
    void validateToken_InvalidToken() {
        // given
        String invalidToken = "invalid.token.here";
        
        // when
        boolean isValid = jwtTokenProvider.validateToken(invalidToken);
        
        // then
        assertThat(isValid).isFalse();
    }

    @Test
    @DisplayName("토큰에서 사용자 ID 추출")
    void getUserIdFromToken_Success() {
        // given
        String token = jwtTokenProvider.generateToken(testUser);
        
        // when
        Long userId = jwtTokenProvider.getUserIdFromToken(token);
        
        // then
        assertThat(userId).isEqualTo(1L);
    }

    @Test
    @DisplayName("토큰에서 이메일 추출")
    void getEmailFromToken_Success() {
        // given
        String token = jwtTokenProvider.generateToken(testUser);
        
        // when
        String email = jwtTokenProvider.getEmailFromToken(token);
        
        // then
        assertThat(email).isEqualTo("test@academy.com");
    }

    @Test
    @DisplayName("토큰에서 역할 추출")
    void getRoleFromToken_Success() {
        // given
        String token = jwtTokenProvider.generateToken(testUser);
        
        // when
        String role = jwtTokenProvider.getRoleFromToken(token);
        
        // then
        assertThat(role).isEqualTo("ADMIN");
    }

    private void setUserId(User user, Long id) {
        try {
            java.lang.reflect.Field field = User.class.getDeclaredField("id");
            field.setAccessible(true);
            field.set(user, id);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```

### 5.2 JwtAuthenticationFilterTest.java

```java
package com.reacademix.reacademix_backend.security;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserRole;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import com.reacademix.reacademix_backend.repository.UserRepository;
import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;

/**
 * JwtAuthenticationFilter 단위 테스트
 */
@ExtendWith(MockitoExtension.class)
class JwtAuthenticationFilterTest {

    @Mock
    private JwtTokenProvider jwtTokenProvider;

    @Mock
    private UserRepository userRepository;

    @Mock
    private HttpServletRequest request;

    @Mock
    private HttpServletResponse response;

    @Mock
    private FilterChain filterChain;

    @InjectMocks
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    private User testUser;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.clearContext();
        
        testUser = User.builder()
            .email("test@academy.com")
            .password("encodedPassword")
            .name("테스트 사용자")
            .role(UserRole.ADMIN)
            .status(UserStatus.ACTIVE)
            .build();
    }

    @Test
    @DisplayName("유효한 토큰으로 인증 성공")
    void doFilterInternal_ValidToken_Success() throws Exception {
        // given
        String token = "valid.jwt.token";
        given(request.getHeader("Authorization")).willReturn("Bearer " + token);
        given(jwtTokenProvider.validateToken(token)).willReturn(true);
        given(jwtTokenProvider.getUserIdFromToken(token)).willReturn(1L);
        given(userRepository.findByIdAndStatus(eq(1L), eq(UserStatus.ACTIVE)))
            .willReturn(Optional.of(testUser));

        // when
        jwtAuthenticationFilter.doFilterInternal(request, response, filterChain);

        // then
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNotNull();
        verify(filterChain).doFilter(request, response);
    }

    @Test
    @DisplayName("Authorization 헤더 없음 - 인증 없이 진행")
    void doFilterInternal_NoHeader_NoAuthentication() throws Exception {
        // given
        given(request.getHeader("Authorization")).willReturn(null);

        // when
        jwtAuthenticationFilter.doFilterInternal(request, response, filterChain);

        // then
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        verify(filterChain).doFilter(request, response);
    }

    @Test
    @DisplayName("유효하지 않은 토큰 - 인증 없이 진행")
    void doFilterInternal_InvalidToken_NoAuthentication() throws Exception {
        // given
        String token = "invalid.jwt.token";
        given(request.getHeader("Authorization")).willReturn("Bearer " + token);
        given(jwtTokenProvider.validateToken(token)).willReturn(false);

        // when
        jwtAuthenticationFilter.doFilterInternal(request, response, filterChain);

        // then
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        verify(filterChain).doFilter(request, response);
    }

    @Test
    @DisplayName("사용자 조회 실패 - 인증 없이 진행")
    void doFilterInternal_UserNotFound_NoAuthentication() throws Exception {
        // given
        String token = "valid.jwt.token";
        given(request.getHeader("Authorization")).willReturn("Bearer " + token);
        given(jwtTokenProvider.validateToken(token)).willReturn(true);
        given(jwtTokenProvider.getUserIdFromToken(token)).willReturn(999L);
        given(userRepository.findByIdAndStatus(eq(999L), eq(UserStatus.ACTIVE)))
            .willReturn(Optional.empty());

        // when
        jwtAuthenticationFilter.doFilterInternal(request, response, filterChain);

        // then
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        verify(filterChain).doFilter(request, response);
    }
}
```

---

## 📝 구현 체크리스트

### 1단계: 의존성 추가 (선행 작업)
- [ ] `build.gradle`에 Spring Security 의존성 추가
- [ ] `build.gradle`에 jjwt 의존성 추가
- [ ] `application.properties`에 JWT 설정 추가

### 2단계: JPA Entity/Repository
- [ ] `User` 엔티티 확인 (BE-AUTH-001에서 생성)
- [ ] `UserRepository`에 `findByIdAndStatus()` 메서드 추가
- [ ] `findActiveUserById()` 메서드 추가 (선택)

### 3단계: JwtTokenProvider 확장
- [ ] `validateToken(String token)` 메서드 추가
- [ ] `getUserIdFromToken(String token)` 메서드 추가
- [ ] `getEmailFromToken(String token)` 메서드 추가
- [ ] `getRoleFromToken(String token)` 메서드 추가
- [ ] `getClaimsFromToken(String token)` 메서드 추가
- [ ] 단위 테스트 작성

### 4단계: Filter 구현
- [ ] `JwtAuthenticationFilter` 클래스 생성
- [ ] `doFilterInternal()` 메서드 구현
- [ ] `extractToken()` 메서드 구현
- [ ] 단위 테스트 작성

### 5단계: EntryPoint 구현
- [ ] `JwtAuthenticationEntryPoint` 클래스 생성
- [ ] `commence()` 메서드 구현
- [ ] `ErrorResponse` DTO 생성
- [ ] `ErrorCode` Enum 확장 (AUTH_005, AUTH_006, AUTH_007 추가)

### 6단계: Security 설정
- [ ] `SecurityConfig` 확장
- [ ] `securityFilterChain()` Bean 설정
- [ ] `corsConfigurationSource()` Bean 설정
- [ ] Public endpoints 정의

### 7단계: 테스트
- [ ] JwtTokenProvider 단위 테스트
- [ ] JwtAuthenticationFilter 단위 테스트
- [ ] SecurityConfig 통합 테스트
- [ ] 성능 테스트 (100ms 이내)

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-12
- **End**: 2025-12-14
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-037
- Related Epic: Authentication & Authorization
