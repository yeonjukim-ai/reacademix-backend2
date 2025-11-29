package com.reacademix.reacademix_backend.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 전역 예외 처리 Handler
 * 애플리케이션에서 발생하는 모든 예외를 일관된 형식으로 처리
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * AuthException 처리 (인증 관련 에러)
     * 
     * @param e AuthException
     * @return ResponseEntity<ErrorResponse>
     */
    @ExceptionHandler(AuthException.class)
    public ResponseEntity<ErrorResponse> handleAuthException(AuthException e) {
        log.warn("인증 에러 발생: {} - {}", e.getErrorCode().getCode(), e.getMessage());
        
        ErrorResponse response = ErrorResponse.of(e.getErrorCode());
        return ResponseEntity
                .status(e.getErrorCode().getHttpStatus())
                .body(response);
    }

    /**
     * MethodArgumentNotValidException 처리 (검증 에러)
     * @Valid 어노테이션 검증 실패 시 발생
     * 
     * @param e MethodArgumentNotValidException
     * @return ResponseEntity<ErrorResponse>
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException e) {
        log.warn("검증 에러 발생: {}", e.getMessage());

        // 필드 에러 목록 생성
        List<ErrorResponse.FieldError> fieldErrors = e.getBindingResult()
                .getFieldErrors()
                .stream()
                .map(error -> ErrorResponse.FieldError.builder()
                        .field(error.getField())
                        .message(error.getDefaultMessage())
                        .build())
                .collect(Collectors.toList());

        ErrorResponse response = ErrorResponse.ofValidation(ErrorCode.VALIDATION_001, fieldErrors);
        return ResponseEntity
                .status(ErrorCode.VALIDATION_001.getHttpStatus())
                .body(response);
    }

    /**
     * IllegalArgumentException 처리 (잘못된 인자 에러)
     * 
     * @param e IllegalArgumentException
     * @return ResponseEntity<ErrorResponse>
     */
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleIllegalArgumentException(IllegalArgumentException e) {
        log.warn("잘못된 인자 에러 발생: {}", e.getMessage());
        
        ErrorResponse response = ErrorResponse.of(ErrorCode.VALIDATION_001);
        return ResponseEntity
                .status(ErrorCode.VALIDATION_001.getHttpStatus())
                .body(response);
    }

    /**
     * 그 외 모든 예외 처리 (시스템 에러)
     * 
     * @param e Exception
     * @return ResponseEntity<ErrorResponse>
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception e) {
        log.error("시스템 에러 발생: {}", e.getMessage(), e);
        
        ErrorResponse response = ErrorResponse.of(ErrorCode.SYSTEM_001);
        return ResponseEntity
                .status(ErrorCode.SYSTEM_001.getHttpStatus())
                .body(response);
    }
}

