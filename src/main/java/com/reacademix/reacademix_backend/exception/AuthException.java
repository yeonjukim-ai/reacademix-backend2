package com.reacademix.reacademix_backend.exception;

import lombok.Getter;

/**
 * 인증 관련 커스텀 예외
 * 로그인, 토큰 검증 등 인증 관련 오류 시 발생
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
public class AuthException extends RuntimeException {
    
    private final ErrorCode errorCode;

    public AuthException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }

    public AuthException(ErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public AuthException(ErrorCode errorCode, Throwable cause) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
    }
}

