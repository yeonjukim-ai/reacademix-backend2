# User 회원가입 기능 코드 스니펫

## 개요

ERD와 Class Diagram을 기반으로 작성된 회원가입 기능의 실제 코드 스니펫입니다.
첫 커밋에 포함할 수 있는 초안 수준의 코드입니다.

**패키지 구조:**
```
com.reacademix.reacademix_backend
├── common
│   └── BaseTimeEntity.java
├── domain
│   └── user
│       ├── User.java
│       ├── UserRole.java
│       └── UserStatus.java
├── repository
│   └── UserRepository.java
├── service
│   └── UserService.java
├── controller
│   └── UserController.java
├── dto
│   ├── request
│   │   └── UserSignupRequest.java
│   └── response
│       └── UserResponse.java
└── config
    ├── SecurityConfig.java
    └── JpaAuditingConfig.java
```

---

## 1. BaseTimeEntity (공통 엔티티)

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
 * 생성 시간과 수정 시간을 자동으로 관리하는 Base Entity
 * 모든 엔티티가 상속받아 사용
 */
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseTimeEntity {

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
```

---

## 2. UserRole (Enum)

```java
package com.reacademix.reacademix_backend.domain.user;

/**
 * 사용자 역할 Enum
 * MVP에서는 ADMIN만 사용하지만, 향후 확장 가능
 */
public enum UserRole {
    ADMIN,      // 관리자 (MVP 기본값)
    MANAGER,    // 관리자 (확장)
    STAFF       // 직원 (확장)
}
```

---

## 3. UserStatus (Enum)

```java
package com.reacademix.reacademix_backend.domain.user;

/**
 * 사용자 상태 Enum
 * MVP에서는 ACTIVE만 사용하지만, 향후 확장 가능
 */
public enum UserStatus {
    ACTIVE,     // 정상 사용 가능 (MVP 기본값)
    INACTIVE,   // 비활성화
    SUSPENDED   // 일시 정지
}
```

---

## 4. User (JPA 엔티티)

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
        this.email = email != null ? email.toLowerCase() : null;  // 이메일 소문자 정규화
        this.password = password;
        this.name = name;
        this.role = role != null ? role : UserRole.ADMIN;
        this.status = status != null ? status : UserStatus.ACTIVE;
    }
}
```

---

## 5. UserRepository (Repository 인터페이스)

```java
package com.reacademix.reacademix_backend.repository;

import com.reacademix.reacademix_backend.domain.user.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * User 엔티티를 위한 Repository 인터페이스
 * Spring Data JPA를 사용하여 데이터베이스 접근
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * 이메일로 사용자 조회
     * @param email 사용자 이메일 (소문자로 정규화되어 저장됨)
     * @return Optional<User> 사용자 정보 (없으면 empty)
     */
    Optional<User> findByEmail(String email);

    /**
     * 이메일 존재 여부 확인 (성능 최적화용)
     * @param email 사용자 이메일
     * @return boolean 이메일 존재 여부
     */
    boolean existsByEmail(String email);
}
```

---

## 6. UserSignupRequest (요청 DTO)

```java
package com.reacademix.reacademix_backend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 회원가입 요청 DTO
 */
@Getter
@NoArgsConstructor
public class UserSignupRequest {

    @NotBlank(message = "이메일은 필수입니다.")
    @Email(message = "올바른 이메일 형식이 아닙니다.")
    @Size(max = 255, message = "이메일은 최대 255자까지 입력 가능합니다.")
    private String email;

    @NotBlank(message = "비밀번호는 필수입니다.")
    @Size(min = 8, max = 128, message = "비밀번호는 8자 이상 128자 이하여야 합니다.")
    private String password;

    @NotBlank(message = "이름은 필수입니다.")
    @Size(min = 2, max = 100, message = "이름은 2자 이상 100자 이하여야 합니다.")
    private String name;
}
```

---

## 7. UserResponse (응답 DTO)

```java
package com.reacademix.reacademix_backend.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

/**
 * 회원가입 응답 DTO
 * 비밀번호는 보안상 포함하지 않음
 */
@Getter
@Builder
public class UserResponse {

    private Long userId;
    private String email;
    private String name;
    private LocalDateTime createdAt;
}
```

---

## 8. UserService (Service 클래스)

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserRole;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import com.reacademix.reacademix_backend.dto.request.UserSignupRequest;
import com.reacademix.reacademix_backend.dto.response.UserResponse;
import com.reacademix.reacademix_backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * User 관련 비즈니스 로직을 처리하는 Service
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    /**
     * 회원가입 처리
     * @param request 회원가입 요청 DTO
     * @return UserResponse 회원가입 응답 DTO
     * @throws RuntimeException 이메일 중복 시 예외 발생
     */
    @Transactional
    public UserResponse signup(UserSignupRequest request) {
        // 이메일 중복 검사
        checkEmailDuplicate(request.getEmail());

        // 비밀번호 암호화
        String encodedPassword = encodePassword(request.getPassword());

        // User 엔티티 생성
        User user = User.builder()
                .email(request.getEmail())
                .password(encodedPassword)
                .name(request.getName())
                .role(UserRole.ADMIN)  // MVP: 기본값 ADMIN
                .status(UserStatus.ACTIVE)  // MVP: 기본값 ACTIVE
                .build();

        // User 저장
        User savedUser = userRepository.save(user);

        // UserResponse로 변환하여 반환
        return buildUserResponse(savedUser);
    }

    /**
     * 이메일 중복 검사
     * @param email 사용자 이메일
     * @throws RuntimeException 이메일이 이미 존재하는 경우
     */
    private void checkEmailDuplicate(String email) {
        if (userRepository.existsByEmail(email.toLowerCase())) {
            throw new RuntimeException("이미 등록된 이메일입니다.");  // TODO: 커스텀 예외로 변경
        }
    }

    /**
     * 비밀번호 암호화
     * @param rawPassword 평문 비밀번호
     * @return String 암호화된 비밀번호 (bcrypt 해시)
     */
    private String encodePassword(String rawPassword) {
        return passwordEncoder.encode(rawPassword);
    }

    /**
     * User 엔티티를 UserResponse DTO로 변환
     * @param user User 엔티티
     * @return UserResponse 회원가입 응답 DTO
     */
    private UserResponse buildUserResponse(User user) {
        return UserResponse.builder()
                .userId(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .createdAt(user.getCreatedAt())
                .build();
    }
}
```

---

## 9. UserController (Controller 클래스)

```java
package com.reacademix.reacademix_backend.controller;

import com.reacademix.reacademix_backend.dto.request.UserSignupRequest;
import com.reacademix.reacademix_backend.dto.response.UserResponse;
import com.reacademix.reacademix_backend.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * User 관련 REST API Controller
 */
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * 회원가입 API
     * @param request 회원가입 요청 DTO
     * @return ResponseEntity<UserResponse> 회원가입 응답 (201 Created)
     */
    @PostMapping
    public ResponseEntity<UserResponse> signup(@Valid @RequestBody UserSignupRequest request) {
        UserResponse response = userService.signup(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
```

---

## 10. SecurityConfig (설정 클래스)

```java
package com.reacademix.reacademix_backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Spring Security 설정
 * PasswordEncoder Bean 등록
 */
@Configuration
public class SecurityConfig {

    /**
     * PasswordEncoder Bean 등록
     * bcrypt 알고리즘 사용 (salt rounds: 10)
     * @return PasswordEncoder BCryptPasswordEncoder 인스턴스
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);  // salt rounds: 10
    }
}
```

---

## 11. JpaAuditingConfig (설정 클래스)

```java
package com.reacademix.reacademix_backend.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * JPA Auditing 설정
 * BaseTimeEntity의 @CreatedDate, @LastModifiedDate 활성화
 */
@Configuration
@EnableJpaAuditing
public class JpaAuditingConfig {
}
```

---

## 주요 특징

### 1. Lombok 활용
- `@Getter`: Getter 메서드 자동 생성
- `@NoArgsConstructor`: 기본 생성자 자동 생성
- `@Builder`: Builder 패턴 지원
- `@RequiredArgsConstructor`: final 필드에 대한 생성자 자동 생성

### 2. JPA 어노테이션
- `@Entity`, `@Table`: 엔티티 및 테이블 매핑
- `@Id`, `@GeneratedValue`: Primary Key 설정
- `@Column`: 컬럼 제약조건 설정
- `@Enumerated`: Enum 타입 매핑

### 3. Spring Validation
- `@Valid`: 요청 데이터 검증
- `@NotBlank`, `@Email`, `@Size`: 필드별 검증 규칙

### 4. Spring Security
- `PasswordEncoder`: 비밀번호 암호화 인터페이스
- `BCryptPasswordEncoder`: bcrypt 구현체

### 5. 트랜잭션 관리
- `@Transactional`: 트랜잭션 관리
- `@Transactional(readOnly = true)`: 읽기 전용 트랜잭션

---

## TODO (향후 개선 사항)

1. **커스텀 예외 처리**
   - `RuntimeException` 대신 `EmailDuplicateException` 등 커스텀 예외 사용
   - 전역 예외 핸들러 구현

2. **에러 응답 구조화**
   - 공통 에러 응답 DTO 생성
   - API 명세서에 맞는 에러 코드 및 메시지

3. **로깅 추가**
   - 회원가입 성공/실패 로깅
   - 예외 발생 시 로깅

4. **테스트 코드 작성**
   - 단위 테스트 (Service, Repository)
   - 통합 테스트 (Controller)

5. **문서화**
   - Swagger/OpenAPI 문서화
   - API 명세서와 일치하도록 문서화

---

**작성일**: 2025-01-27  
**버전**: 1.0 (초안)  
**작성자**: Backend Development Team

