package com.reacademix.reacademix_backend.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.reacademix.reacademix_backend.dto.request.LoginRequestDto;
import com.reacademix.reacademix_backend.dto.response.LoginResponseDto;
import com.reacademix.reacademix_backend.exception.AuthException;
import com.reacademix.reacademix_backend.exception.ErrorCode;
import com.reacademix.reacademix_backend.exception.GlobalExceptionHandler;
import com.reacademix.reacademix_backend.service.AuthService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * AuthController 통합 테스트
 * 
 * @author Backend Team
 * @version 1.0
 */
@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    @Mock
    private AuthService authService;

    @InjectMocks
    private AuthController authController;

    private MockMvc mockMvc;
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(authController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();
        objectMapper = new ObjectMapper();
    }

    @Nested
    @DisplayName("POST /api/v1/auth/login")
    class LoginApiTest {

        @Test
        @DisplayName("성공: 올바른 요청으로 로그인 (200 OK)")
        void login_Success_Returns200() throws Exception {
            // given
            LoginRequestDto request = LoginRequestDto.builder()
                    .email("test@academy.com")
                    .password("SecurePass123!")
                    .build();

            LoginResponseDto response = LoginResponseDto.builder()
                    .token("jwt-token-string")
                    .tokenType("Bearer")
                    .expiresIn(86400L)
                    .user(LoginResponseDto.UserInfo.builder()
                            .userId(1L)
                            .email("test@academy.com")
                            .name("테스트 사용자")
                            .build())
                    .build();

            given(authService.login(any(LoginRequestDto.class))).willReturn(response);

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andDo(print())
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.success").value(true))
                    .andExpect(jsonPath("$.message").value("로그인에 성공했습니다."))
                    .andExpect(jsonPath("$.data.token").value("jwt-token-string"))
                    .andExpect(jsonPath("$.data.tokenType").value("Bearer"))
                    .andExpect(jsonPath("$.data.expiresIn").value(86400))
                    .andExpect(jsonPath("$.data.user.userId").value(1))
                    .andExpect(jsonPath("$.data.user.email").value("test@academy.com"))
                    .andExpect(jsonPath("$.data.user.name").value("테스트 사용자"));
        }

        @Test
        @DisplayName("실패: 이메일 누락 (400 Bad Request)")
        void login_Fail_MissingEmail() throws Exception {
            // given
            String requestBody = "{\"password\": \"SecurePass123!\"}";

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(requestBody))
                    .andDo(print())
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.success").value(false))
                    .andExpect(jsonPath("$.error.code").value("VALIDATION_001"));
        }

        @Test
        @DisplayName("실패: 잘못된 이메일 형식 (400 Bad Request)")
        void login_Fail_InvalidEmailFormat() throws Exception {
            // given
            LoginRequestDto request = LoginRequestDto.builder()
                    .email("invalid-email")
                    .password("SecurePass123!")
                    .build();

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andDo(print())
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.success").value(false))
                    .andExpect(jsonPath("$.error.code").value("VALIDATION_001"));
        }

        @Test
        @DisplayName("실패: 비밀번호 8자 미만 (400 Bad Request)")
        void login_Fail_PasswordTooShort() throws Exception {
            // given
            LoginRequestDto request = LoginRequestDto.builder()
                    .email("test@academy.com")
                    .password("short")
                    .build();

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andDo(print())
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.success").value(false))
                    .andExpect(jsonPath("$.error.code").value("VALIDATION_001"));
        }

        @Test
        @DisplayName("실패: 존재하지 않는 이메일 (401 Unauthorized)")
        void login_Fail_UserNotFound() throws Exception {
            // given
            LoginRequestDto request = LoginRequestDto.builder()
                    .email("notfound@academy.com")
                    .password("SecurePass123!")
                    .build();

            given(authService.login(any(LoginRequestDto.class)))
                    .willThrow(new AuthException(ErrorCode.AUTH_002));

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andDo(print())
                    .andExpect(status().isUnauthorized())
                    .andExpect(jsonPath("$.success").value(false))
                    .andExpect(jsonPath("$.error.code").value("AUTH_002"))
                    .andExpect(jsonPath("$.error.message").value("이메일 또는 비밀번호가 올바르지 않습니다."));
        }

        @Test
        @DisplayName("실패: 비밀번호 불일치 (401 Unauthorized)")
        void login_Fail_WrongPassword() throws Exception {
            // given
            LoginRequestDto request = LoginRequestDto.builder()
                    .email("test@academy.com")
                    .password("WrongPassword!")
                    .build();

            given(authService.login(any(LoginRequestDto.class)))
                    .willThrow(new AuthException(ErrorCode.AUTH_003));

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andDo(print())
                    .andExpect(status().isUnauthorized())
                    .andExpect(jsonPath("$.success").value(false))
                    .andExpect(jsonPath("$.error.code").value("AUTH_003"))
                    .andExpect(jsonPath("$.error.message").value("이메일 또는 비밀번호가 올바르지 않습니다."));
        }

        @Test
        @DisplayName("실패: 비활성화된 계정 (401 Unauthorized)")
        void login_Fail_InactiveAccount() throws Exception {
            // given
            LoginRequestDto request = LoginRequestDto.builder()
                    .email("inactive@academy.com")
                    .password("SecurePass123!")
                    .build();

            given(authService.login(any(LoginRequestDto.class)))
                    .willThrow(new AuthException(ErrorCode.AUTH_004));

            // when & then
            mockMvc.perform(post("/api/v1/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andDo(print())
                    .andExpect(status().isUnauthorized())
                    .andExpect(jsonPath("$.success").value(false))
                    .andExpect(jsonPath("$.error.code").value("AUTH_004"))
                    .andExpect(jsonPath("$.error.message").value("계정이 비활성화되었습니다."));
        }
    }
}

