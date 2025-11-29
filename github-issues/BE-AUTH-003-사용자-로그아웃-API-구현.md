# 사용자 로그아웃 API 구현

- **Type**: Functional
- **Key**: BE-AUTH-003
- **REQ / Epic**: REQ-FUNC-036
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002

## 📌 Description

사용자 로그아웃 API를 구현합니다. JWT 토큰 기반 인증에서 로그아웃은 클라이언트 측에서 토큰을 삭제하는 방식으로 처리하지만, 보안 강화를 위해 선택적으로 토큰 블랙리스트 기능을 구현할 수 있습니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `POST /api/v1/auth/logout` 엔드포인트 구현
- [ ] 인증된 사용자만 접근 가능
- [ ] 로그아웃 성공 응답 반환

### 선택적 기능 (Phase 2)
- [ ] 토큰 블랙리스트 저장소 구현 (Redis 권장)
- [ ] 로그아웃 시 토큰 블랙리스트 등록
- [ ] JWT 검증 시 블랙리스트 확인

### DTO 클래스
- [ ] `LogoutResponseDto` 클래스 생성

### 테스트
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

---

## 📋 API 명세서

### 1. Endpoint

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `POST` |
| **URI** | `/api/v1/auth/logout` |
| **Content-Type** | `application/json` |
| **인증 필요** | ✅ (JWT 토큰 필수) |

**요청 예시:**
```http
POST /api/v1/auth/logout HTTP/1.1
Host: api.reacademix.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Response Body

#### 2.1 성공 응답 (200 OK)

```json
{
  "success": true,
  "data": null,
  "message": "로그아웃 되었습니다."
}
```

#### 2.2 실패 응답

| HTTP Status | 에러 코드 | 메시지 | 발생 조건 |
|-------------|----------|--------|----------|
| `401 Unauthorized` | `AUTH_001` | "인증 토큰이 필요합니다." | 토큰 없음 |
| `401 Unauthorized` | `AUTH_005` | "토큰이 만료되었습니다." | 토큰 만료 |

---

## 🔄 Sequence Diagram

### MVP 버전 (클라이언트 측 토큰 삭제)

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Controller as AuthController
    participant Service as AuthService

    Client->>+Filter: POST /api/v1/auth/logout<br/>Authorization: Bearer token
    
    Note over Filter: JWT 토큰 검증
    Filter->>Filter: validateToken() ✓
    Filter->>Controller: 인증 완료
    
    Controller->>+Service: logout()
    
    Note over Service: MVP: 특별한 처리 없음<br/>(클라이언트가 토큰 삭제)
    Service->>Service: 로그아웃 이벤트 로깅 (선택)
    
    Service-->>-Controller: void
    Controller-->>-Client: HTTP 200 OK
    
    Note over Client: 1. 응답 수신<br/>2. localStorage/sessionStorage에서<br/>   토큰 삭제<br/>3. 로그인 페이지로 이동
```

### Phase 2 버전 (토큰 블랙리스트)

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Controller as AuthController
    participant Service as AuthService
    participant Redis as Redis (Blacklist)

    Client->>+Filter: POST /api/v1/auth/logout<br/>Authorization: Bearer token
    
    Filter->>Filter: validateToken() ✓
    Filter->>Controller: 인증 완료, token 전달
    
    Controller->>+Service: logout(token)
    
    Note over Service: 토큰 만료 시간 계산
    Service->>Service: exp claim에서 TTL 계산
    
    Service->>+Redis: SET blacklist:{token} "logout"<br/>EX {TTL}
    Redis-->>-Service: OK
    
    Note over Redis: 토큰 만료 시간까지만<br/>블랙리스트 유지
    
    Service-->>-Controller: void
    Controller-->>-Client: HTTP 200 OK
    
    Note over Client: 이후 해당 토큰으로 요청 시<br/>블랙리스트에서 거부됨
```

---

## 💻 ORM 예제 코드

### AuthController.java (추가)

```java
/**
 * 사용자 로그아웃 API
 * 
 * @param request HTTP 요청 (Authorization 헤더에서 토큰 추출)
 * @return ResponseEntity<ApiResponse<Void>>
 */
@PostMapping("/logout")
@Operation(summary = "로그아웃", description = "사용자 로그아웃을 처리합니다.")
public ResponseEntity<ApiResponse<Void>> logout(HttpServletRequest request) {
    
    // Authorization 헤더에서 토큰 추출 (선택적)
    String token = extractToken(request);
    
    log.info("로그아웃 요청");
    
    authService.logout(token);
    
    return ResponseEntity.ok(ApiResponse.success("로그아웃 되었습니다."));
}

private String extractToken(HttpServletRequest request) {
    String bearerToken = request.getHeader("Authorization");
    if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
        return bearerToken.substring(7);
    }
    return null;
}
```

### AuthService.java (추가)

```java
/**
 * 로그아웃 처리
 * MVP: 로깅만 수행 (클라이언트에서 토큰 삭제)
 * Phase 2: 토큰 블랙리스트 등록
 * 
 * @param token JWT 토큰 (선택적)
 */
public void logout(String token) {
    // MVP: 로깅만 수행
    log.info("사용자 로그아웃 처리");
    
    // Phase 2: 토큰 블랙리스트 등록
    // if (token != null) {
    //     tokenBlacklistService.addToBlacklist(token);
    // }
}
```

### Phase 2: TokenBlacklistService.java

```java
package com.reacademix.reacademix_backend.security;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

/**
 * 토큰 블랙리스트 서비스 (Phase 2)
 * Redis를 사용하여 로그아웃된 토큰 관리
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class TokenBlacklistService {

    private final StringRedisTemplate redisTemplate;
    private final JwtTokenProvider jwtTokenProvider;
    
    private static final String BLACKLIST_PREFIX = "blacklist:";

    /**
     * 토큰을 블랙리스트에 등록
     * 토큰 만료 시간까지만 유지
     */
    public void addToBlacklist(String token) {
        try {
            // 토큰 만료 시간 계산
            long expirationTime = jwtTokenProvider.getExpirationFromToken(token);
            long now = System.currentTimeMillis();
            long ttl = (expirationTime - now) / 1000; // 초 단위
            
            if (ttl > 0) {
                String key = BLACKLIST_PREFIX + token;
                redisTemplate.opsForValue().set(key, "logout", ttl, TimeUnit.SECONDS);
                log.info("토큰 블랙리스트 등록: TTL={}s", ttl);
            }
        } catch (Exception e) {
            log.error("블랙리스트 등록 실패: {}", e.getMessage());
        }
    }

    /**
     * 토큰이 블랙리스트에 있는지 확인
     */
    public boolean isBlacklisted(String token) {
        String key = BLACKLIST_PREFIX + token;
        return Boolean.TRUE.equals(redisTemplate.hasKey(key));
    }
}
```

---

## 📝 구현 체크리스트

### MVP (Phase 1)
- [ ] `AuthController.logout()` 구현
- [ ] `AuthService.logout()` 구현
- [ ] 로깅 추가
- [ ] 단위 테스트

### Phase 2 (선택)
- [ ] Redis 의존성 추가
- [ ] `TokenBlacklistService` 구현
- [ ] `JwtAuthenticationFilter`에 블랙리스트 확인 로직 추가
- [ ] 통합 테스트

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-16
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-036
- Related Epic: Authentication & Authorization
