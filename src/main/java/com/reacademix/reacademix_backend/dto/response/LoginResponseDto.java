package com.reacademix.reacademix_backend.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 로그인 응답 DTO
 * 로그인 성공 시 JWT 토큰과 사용자 정보를 반환
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LoginResponseDto {

    /** JWT 토큰 */
    private String token;
    
    /** 토큰 타입 (항상 "Bearer") */
    private String tokenType;
    
    /** 토큰 만료 시간 (초 단위, 기본 86400 = 24시간) */
    private Long expiresIn;
    
    /** 사용자 정보 */
    private UserInfo user;

    /**
     * 사용자 정보 내부 클래스
     */
    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UserInfo {
        /** 사용자 고유 ID */
        private Long userId;
        
        /** 사용자 이메일 */
        private String email;
        
        /** 사용자 이름 */
        private String name;
    }
}

