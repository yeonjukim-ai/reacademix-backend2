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

