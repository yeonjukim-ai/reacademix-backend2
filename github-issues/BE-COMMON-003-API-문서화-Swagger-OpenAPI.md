# API 문서화 (Swagger/OpenAPI)

- **Type**: Non-Functional
- **Key**: BE-COMMON-003
- **REQ / Epic**: Common Infrastructure
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-001

## 📌 Description

SpringDoc OpenAPI를 사용하여 API 문서를 자동 생성합니다. Swagger UI를 통해 API를 테스트하고, API 스펙을 확인할 수 있습니다.

## ✅ Acceptance Criteria

### OpenAPI 설정
- [ ] SpringDoc OpenAPI 의존성 추가
- [ ] `SwaggerConfig` 설정 클래스 생성
- [ ] API 정보 (title, description, version) 설정
- [ ] JWT 인증 설정 (SecurityScheme)

### API 문서화
- [ ] 모든 Controller에 `@Tag` 어노테이션 추가
- [ ] 모든 엔드포인트에 `@Operation` 어노테이션 추가
- [ ] Request/Response DTO에 `@Schema` 어노테이션 추가
- [ ] 에러 응답 예시 문서화

### 접근 설정
- [ ] Swagger UI 접근 경로 설정 (`/swagger-ui.html`)
- [ ] 개발 환경에서만 Swagger UI 활성화
- [ ] API 문서 JSON 경로 설정 (`/v3/api-docs`)

---

## 💻 구현 코드

### SwaggerConfig.java

```java
package com.reacademix.reacademix_backend.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

/**
 * Swagger/OpenAPI 설정
 */
@Configuration
public class SwaggerConfig {

    private static final String SECURITY_SCHEME_NAME = "bearerAuth";

    @Value("${spring.profiles.active:dev}")
    private String activeProfile;

    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
            .info(apiInfo())
            .servers(servers())
            .addSecurityItem(new SecurityRequirement().addList(SECURITY_SCHEME_NAME))
            .components(new Components()
                .addSecuritySchemes(SECURITY_SCHEME_NAME, securityScheme()));
    }

    private Info apiInfo() {
        return new Info()
            .title("ReAcademix Backend API")
            .description("""
                ## 📚 ReAcademix Backend API 문서
                
                도심형 통학 관리형 재수 학원을 위한 성과 리포트 자동화 SaaS 백엔드 API입니다.
                
                ### 주요 기능
                - 🔐 **인증**: JWT 기반 로그인/로그아웃
                - 👨‍🎓 **학생 관리**: 학생 검색, 상세 조회
                - 📊 **리포트 생성**: 학생별 성과 리포트 PDF 생성
                - 📧 **리포트 전송**: 이메일 전송 및 다운로드
                - 📁 **데이터 통합**: CSV/Excel 파일 업로드
                
                ### 인증 방법
                1. `/api/v1/auth/login` API로 로그인
                2. 응답의 `token` 값 복사
                3. 우측 상단 **Authorize** 버튼 클릭
                4. `Bearer {token}` 형식으로 입력
                """)
            .version("v1.0.0")
            .contact(new Contact()
                .name("ReAcademix Backend Team")
                .email("backend@reacademix.com")
                .url("https://reacademix.com"))
            .license(new License()
                .name("Private License")
                .url("https://reacademix.com/license"));
    }

    private List<Server> servers() {
        if ("prod".equals(activeProfile)) {
            return List.of(
                new Server().url("https://api.reacademix.com").description("Production Server")
            );
        }
        return List.of(
            new Server().url("http://localhost:8080").description("Local Development Server")
        );
    }

    private SecurityScheme securityScheme() {
        return new SecurityScheme()
            .type(SecurityScheme.Type.HTTP)
            .scheme("bearer")
            .bearerFormat("JWT")
            .in(SecurityScheme.In.HEADER)
            .name("Authorization")
            .description("JWT 토큰을 입력하세요. 형식: Bearer {token}");
    }
}
```

### Controller 예시 (어노테이션 적용)

```java
@Tag(name = "Auth", description = "인증 관련 API")
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    @Operation(
        summary = "로그인",
        description = "이메일과 비밀번호로 로그인하여 JWT 토큰을 발급받습니다.",
        responses = {
            @ApiResponse(responseCode = "200", description = "로그인 성공",
                content = @Content(schema = @Schema(implementation = LoginResponseDto.class))),
            @ApiResponse(responseCode = "401", description = "인증 실패",
                content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
        }
    )
    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponseDto>> login(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                description = "로그인 정보",
                required = true,
                content = @Content(schema = @Schema(implementation = LoginRequestDto.class))
            )
            @Valid @RequestBody LoginRequestDto request) {
        // ...
    }
}
```

### DTO 예시 (Schema 적용)

```java
@Schema(description = "로그인 요청")
@Getter
@Builder
public class LoginRequestDto {

    @Schema(description = "이메일", example = "admin@academy.com", required = true)
    @NotBlank
    @Email
    private String email;

    @Schema(description = "비밀번호", example = "SecurePass123!", required = true, minLength = 8)
    @NotBlank
    @Size(min = 8)
    private String password;
}
```

### application.properties 설정

```properties
# Swagger/OpenAPI
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.enabled=true
springdoc.swagger-ui.tags-sorter=alpha
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.display-request-duration=true

# 운영 환경에서 비활성화
# spring.profiles.active=prod 시 false로 설정
```

---

## 📝 구현 체크리스트

### 1단계: 의존성 및 설정
- [ ] SpringDoc 의존성 추가
- [ ] `SwaggerConfig` 생성
- [ ] `application.properties` 설정

### 2단계: Controller 문서화
- [ ] 모든 Controller에 `@Tag` 추가
- [ ] 모든 엔드포인트에 `@Operation` 추가
- [ ] 응답 코드별 `@ApiResponse` 추가

### 3단계: DTO 문서화
- [ ] Request DTO에 `@Schema` 추가
- [ ] Response DTO에 `@Schema` 추가
- [ ] 예시 값 추가

### 4단계: 검증
- [ ] Swagger UI 접근 확인
- [ ] API 테스트 기능 확인
- [ ] JWT 인증 테스트

---

## ⏱ 일정(Timeline)

- **Start**: 2025-11-30
- **End**: 2025-12-02
- **Lane**: Prerequisites

## 🔗 Traceability

- Related SRS: N/A
- Related Epic: Common Infrastructure
