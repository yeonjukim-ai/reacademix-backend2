package com.reacademix.reacademix_backend.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * API 표준 응답 DTO
 * 모든 API 응답을 일관된 형식으로 래핑
 * 
 * @param <T> 응답 데이터 타입
 * @author Backend Team
 * @version 1.0
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {

    /** 요청 성공 여부 */
    private boolean success;
    
    /** 응답 데이터 */
    private T data;
    
    /** 응답 메시지 */
    private String message;

    /**
     * 성공 응답 생성 (데이터 + 메시지)
     * 
     * @param data 응답 데이터
     * @param message 응답 메시지
     * @param <T> 데이터 타입
     * @return ApiResponse 인스턴스
     */
    public static <T> ApiResponse<T> success(T data, String message) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .message(message)
                .build();
    }

    /**
     * 성공 응답 생성 (데이터만)
     * 
     * @param data 응답 데이터
     * @param <T> 데이터 타입
     * @return ApiResponse 인스턴스
     */
    public static <T> ApiResponse<T> success(T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .build();
    }

    /**
     * 성공 응답 생성 (메시지만)
     * 
     * @param message 응답 메시지
     * @param <T> 데이터 타입
     * @return ApiResponse 인스턴스
     */
    public static <T> ApiResponse<T> success(String message) {
        return ApiResponse.<T>builder()
                .success(true)
                .message(message)
                .build();
    }
}

