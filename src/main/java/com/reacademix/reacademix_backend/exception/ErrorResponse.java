package com.reacademix.reacademix_backend.exception;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 에러 응답 DTO
 * API 에러 발생 시 표준화된 응답 형식 제공
 * 
 * @author Backend Team
 * @version 1.0
 */
@Getter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    
    private final boolean success;
    private final Error error;
    private final LocalDateTime timestamp;

    @Getter
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class Error {
        private final String code;
        private final String message;
        private final ErrorDetails details;
    }

    @Getter
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class ErrorDetails {
        private final String field;
        private final Object rejectedValue;
        private final List<FieldError> errors;
    }

    @Getter
    @Builder
    public static class FieldError {
        private final String field;
        private final String message;
    }

    /**
     * ErrorCode로부터 ErrorResponse 생성
     * 
     * @param errorCode 에러 코드
     * @return ErrorResponse 인스턴스
     */
    public static ErrorResponse of(ErrorCode errorCode) {
        return ErrorResponse.builder()
                .success(false)
                .error(Error.builder()
                        .code(errorCode.getCode())
                        .message(errorCode.getMessage())
                        .build())
                .timestamp(LocalDateTime.now())
                .build();
    }

    /**
     * ErrorCode와 상세 내용으로 ErrorResponse 생성
     * 
     * @param errorCode 에러 코드
     * @param details 에러 상세 정보
     * @return ErrorResponse 인스턴스
     */
    public static ErrorResponse of(ErrorCode errorCode, ErrorDetails details) {
        return ErrorResponse.builder()
                .success(false)
                .error(Error.builder()
                        .code(errorCode.getCode())
                        .message(errorCode.getMessage())
                        .details(details)
                        .build())
                .timestamp(LocalDateTime.now())
                .build();
    }

    /**
     * 검증 에러용 ErrorResponse 생성
     * 
     * @param errorCode 에러 코드
     * @param fieldErrors 필드 에러 목록
     * @return ErrorResponse 인스턴스
     */
    public static ErrorResponse ofValidation(ErrorCode errorCode, List<FieldError> fieldErrors) {
        return ErrorResponse.builder()
                .success(false)
                .error(Error.builder()
                        .code(errorCode.getCode())
                        .message(errorCode.getMessage())
                        .details(ErrorDetails.builder()
                                .errors(fieldErrors)
                                .build())
                        .build())
                .timestamp(LocalDateTime.now())
                .build();
    }
}

