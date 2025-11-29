package com.reacademix.reacademix_backend.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

/**
 * 에러 코드 Enum
 * 애플리케이션 전체에서 사용되는 표준 에러 코드 정의
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    
    // 인증 관련 에러 (AUTH_XXX) - 401 Unauthorized
    AUTH_001("AUTH_001", "인증이 필요합니다.", HttpStatus.UNAUTHORIZED),
    AUTH_002("AUTH_002", "이메일 또는 비밀번호가 올바르지 않습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_003("AUTH_003", "이메일 또는 비밀번호가 올바르지 않습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_004("AUTH_004", "계정이 비활성화되었습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_005("AUTH_005", "토큰이 만료되었습니다.", HttpStatus.UNAUTHORIZED),
    AUTH_006("AUTH_006", "유효하지 않은 토큰입니다.", HttpStatus.UNAUTHORIZED),
    
    // 검증 관련 에러 (VALIDATION_XXX) - 400 Bad Request
    VALIDATION_001("VALIDATION_001", "입력 데이터 검증에 실패했습니다.", HttpStatus.BAD_REQUEST),
    VALIDATION_002("VALIDATION_002", "올바른 이메일 형식이 아닙니다.", HttpStatus.BAD_REQUEST),
    VALIDATION_003("VALIDATION_003", "비밀번호는 최소 8자 이상이어야 합니다.", HttpStatus.BAD_REQUEST),
    
    // 리소스 관련 에러 (RESOURCE_XXX) - 404 Not Found
    RESOURCE_001("RESOURCE_001", "요청한 리소스를 찾을 수 없습니다.", HttpStatus.NOT_FOUND),
    RESOURCE_002("RESOURCE_002", "사용자를 찾을 수 없습니다.", HttpStatus.NOT_FOUND),
    
    // 시스템 에러 (SYSTEM_XXX) - 500 Internal Server Error
    SYSTEM_001("SYSTEM_001", "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요.", HttpStatus.INTERNAL_SERVER_ERROR),
    SYSTEM_002("SYSTEM_002", "데이터베이스 오류가 발생했습니다.", HttpStatus.INTERNAL_SERVER_ERROR),
    SYSTEM_003("SYSTEM_003", "토큰 생성에 실패했습니다.", HttpStatus.INTERNAL_SERVER_ERROR);

    private final String code;
    private final String message;
    private final HttpStatus httpStatus;
}

