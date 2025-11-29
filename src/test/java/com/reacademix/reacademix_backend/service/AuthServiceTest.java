package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserRole;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import com.reacademix.reacademix_backend.dto.request.LoginRequestDto;
import com.reacademix.reacademix_backend.dto.response.LoginResponseDto;
import com.reacademix.reacademix_backend.exception.AuthException;
import com.reacademix.reacademix_backend.exception.ErrorCode;
import com.reacademix.reacademix_backend.repository.UserRepository;
import com.reacademix.reacademix_backend.security.JwtTokenProvider;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;

/**
 * AuthService 단위 테스트
 * 
 * @author Backend Team
 * @version 1.0
 */
@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtTokenProvider jwtTokenProvider;

    @InjectMocks
    private AuthService authService;

    private User testUser;
    private LoginRequestDto loginRequest;

    @BeforeEach
    void setUp() {
        // 테스트용 사용자 생성
        testUser = User.builder()
                .email("test@academy.com")
                .password("$2a$10$encodedPassword")  // bcrypt 해시
                .name("테스트 사용자")
                .role(UserRole.ADMIN)
                .status(UserStatus.ACTIVE)
                .build();

        // 테스트용 로그인 요청 생성
        loginRequest = LoginRequestDto.builder()
                .email("test@academy.com")
                .password("SecurePass123!")
                .build();
    }

    @Nested
    @DisplayName("로그인 테스트")
    class LoginTest {

        @Test
        @DisplayName("성공: 올바른 이메일과 비밀번호로 로그인")
        void login_Success() {
            // given
            given(userRepository.findByEmail("test@academy.com"))
                    .willReturn(Optional.of(testUser));
            given(passwordEncoder.matches("SecurePass123!", testUser.getPassword()))
                    .willReturn(true);
            given(jwtTokenProvider.generateToken(testUser))
                    .willReturn("jwt-token-string");
            given(jwtTokenProvider.getExpirationTimeInSeconds())
                    .willReturn(86400L);

            // when
            LoginResponseDto response = authService.login(loginRequest);

            // then
            assertThat(response).isNotNull();
            assertThat(response.getToken()).isEqualTo("jwt-token-string");
            assertThat(response.getTokenType()).isEqualTo("Bearer");
            assertThat(response.getExpiresIn()).isEqualTo(86400L);
            assertThat(response.getUser()).isNotNull();
            assertThat(response.getUser().getEmail()).isEqualTo("test@academy.com");
            assertThat(response.getUser().getName()).isEqualTo("테스트 사용자");

            verify(userRepository).findByEmail("test@academy.com");
            verify(passwordEncoder).matches("SecurePass123!", testUser.getPassword());
            verify(jwtTokenProvider).generateToken(testUser);
        }

        @Test
        @DisplayName("성공: 이메일 대소문자 구분 없이 로그인")
        void login_Success_CaseInsensitiveEmail() {
            // given
            LoginRequestDto upperCaseRequest = LoginRequestDto.builder()
                    .email("TEST@ACADEMY.COM")
                    .password("SecurePass123!")
                    .build();

            given(userRepository.findByEmail("test@academy.com"))
                    .willReturn(Optional.of(testUser));
            given(passwordEncoder.matches("SecurePass123!", testUser.getPassword()))
                    .willReturn(true);
            given(jwtTokenProvider.generateToken(testUser))
                    .willReturn("jwt-token-string");
            given(jwtTokenProvider.getExpirationTimeInSeconds())
                    .willReturn(86400L);

            // when
            LoginResponseDto response = authService.login(upperCaseRequest);

            // then
            assertThat(response).isNotNull();
            verify(userRepository).findByEmail("test@academy.com");
        }

        @Test
        @DisplayName("실패: 존재하지 않는 이메일 (AUTH_002)")
        void login_Fail_UserNotFound() {
            // given
            given(userRepository.findByEmail(anyString()))
                    .willReturn(Optional.empty());

            // when & then
            assertThatThrownBy(() -> authService.login(loginRequest))
                    .isInstanceOf(AuthException.class)
                    .satisfies(e -> {
                        AuthException authException = (AuthException) e;
                        assertThat(authException.getErrorCode()).isEqualTo(ErrorCode.AUTH_002);
                    });
        }

        @Test
        @DisplayName("실패: 비밀번호 불일치 (AUTH_003)")
        void login_Fail_WrongPassword() {
            // given
            given(userRepository.findByEmail("test@academy.com"))
                    .willReturn(Optional.of(testUser));
            given(passwordEncoder.matches(anyString(), anyString()))
                    .willReturn(false);

            // when & then
            assertThatThrownBy(() -> authService.login(loginRequest))
                    .isInstanceOf(AuthException.class)
                    .satisfies(e -> {
                        AuthException authException = (AuthException) e;
                        assertThat(authException.getErrorCode()).isEqualTo(ErrorCode.AUTH_003);
                    });
        }

        @Test
        @DisplayName("실패: 비활성화된 계정 (AUTH_004)")
        void login_Fail_InactiveAccount() {
            // given
            User inactiveUser = User.builder()
                    .email("inactive@academy.com")
                    .password("$2a$10$encodedPassword")
                    .name("비활성 사용자")
                    .role(UserRole.ADMIN)
                    .status(UserStatus.INACTIVE)
                    .build();

            given(userRepository.findByEmail("test@academy.com"))
                    .willReturn(Optional.of(inactiveUser));

            // when & then
            assertThatThrownBy(() -> authService.login(loginRequest))
                    .isInstanceOf(AuthException.class)
                    .satisfies(e -> {
                        AuthException authException = (AuthException) e;
                        assertThat(authException.getErrorCode()).isEqualTo(ErrorCode.AUTH_004);
                    });
        }

        @Test
        @DisplayName("실패: 정지된 계정 (AUTH_004)")
        void login_Fail_SuspendedAccount() {
            // given
            User suspendedUser = User.builder()
                    .email("suspended@academy.com")
                    .password("$2a$10$encodedPassword")
                    .name("정지된 사용자")
                    .role(UserRole.ADMIN)
                    .status(UserStatus.SUSPENDED)
                    .build();

            given(userRepository.findByEmail("test@academy.com"))
                    .willReturn(Optional.of(suspendedUser));

            // when & then
            assertThatThrownBy(() -> authService.login(loginRequest))
                    .isInstanceOf(AuthException.class)
                    .satisfies(e -> {
                        AuthException authException = (AuthException) e;
                        assertThat(authException.getErrorCode()).isEqualTo(ErrorCode.AUTH_004);
                    });
        }
    }
}

