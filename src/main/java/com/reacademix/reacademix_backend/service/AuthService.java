package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.domain.user.UserStatus;
import com.reacademix.reacademix_backend.dto.request.LoginRequestDto;
import com.reacademix.reacademix_backend.dto.response.LoginResponseDto;
import com.reacademix.reacademix_backend.exception.AuthException;
import com.reacademix.reacademix_backend.exception.ErrorCode;
import com.reacademix.reacademix_backend.repository.UserRepository;
import com.reacademix.reacademix_backend.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 인증 관련 비즈니스 로직을 처리하는 Service 클래스
 * 로그인, 로그아웃 등 인증 관련 기능 제공
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    /**
     * 사용자 로그인 처리
     * 
     * 처리 순서:
     * 1. 이메일 정규화 (소문자 변환)
     * 2. 사용자 조회 (Repository Layer 호출)
     * 3. 계정 상태 확인 (ACTIVE 여부)
     * 4. 비밀번호 검증 (BCrypt)
     * 5. JWT 토큰 생성
     * 6. 응답 DTO 생성
     * 
     * @param request 로그인 요청 DTO (email, password)
     * @return LoginResponseDto 로그인 응답 (token, user 정보)
     * @throws AuthException 인증 실패 시 (AUTH_002, AUTH_003, AUTH_004)
     */
    @Transactional
    public LoginResponseDto login(LoginRequestDto request) {
        // 1. 이메일 정규화 (소문자 변환 및 공백 제거)
        String email = request.getEmail().toLowerCase().trim();
        log.debug("로그인 시도: {}", email);

        // 2. 사용자 조회 (Repository Layer 호출)
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> {
                    log.warn("로그인 실패: 이메일 없음 - {}", email);
                    return new AuthException(ErrorCode.AUTH_002);
                });

        // 3. 계정 상태 확인 (ACTIVE 여부)
        if (user.getStatus() != UserStatus.ACTIVE) {
            log.warn("로그인 실패: 계정 비활성화 - {}, 상태: {}", email, user.getStatus());
            throw new AuthException(ErrorCode.AUTH_004);
        }

        // 4. 비밀번호 검증 (BCrypt 사용)
        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            log.warn("로그인 실패: 비밀번호 불일치 - {}", email);
            throw new AuthException(ErrorCode.AUTH_003);
        }

        // 5. JWT 토큰 생성
        String token = jwtTokenProvider.generateToken(user);
        long expiresIn = jwtTokenProvider.getExpirationTimeInSeconds();

        log.info("로그인 성공: {}", email);

        // 6. 응답 DTO 생성 및 반환
        return LoginResponseDto.builder()
                .token(token)
                .tokenType("Bearer")
                .expiresIn(expiresIn)
                .user(LoginResponseDto.UserInfo.builder()
                        .userId(user.getId())
                        .email(user.getEmail())
                        .name(user.getName())
                        .build())
                .build();
    }
}

