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

