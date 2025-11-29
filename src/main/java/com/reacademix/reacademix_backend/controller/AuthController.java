package com.reacademix.reacademix_backend.controller;

import com.reacademix.reacademix_backend.dto.request.LoginRequestDto;
import com.reacademix.reacademix_backend.dto.response.ApiResponse;
import com.reacademix.reacademix_backend.dto.response.LoginResponseDto;
import com.reacademix.reacademix_backend.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 인증 관련 REST API Controller
 * 로그인, 로그아웃 등 인증 관련 엔드포인트 제공
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * 사용자 로그인 API
     * 
     * @param request 로그인 요청 DTO (email, password)
     * @return ResponseEntity<ApiResponse<LoginResponseDto>> 로그인 응답
     * 
     * @apiNote
     * - HTTP Method: POST
     * - URI: /api/v1/auth/login
     * - Content-Type: application/json
     * - 인증 필요: 아니오 (로그인 API)
     * 
     * @success 200 OK - 로그인 성공, JWT 토큰 및 사용자 정보 반환
     * @error 400 Bad Request - 요청 데이터 검증 실패 (이메일 형식, 비밀번호 길이)
     * @error 401 Unauthorized - 이메일 또는 비밀번호 불일치, 계정 비활성화
     * @error 500 Internal Server Error - 시스템 오류
     */
    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponseDto>> login(
            @Valid @RequestBody LoginRequestDto request) {

        log.info("로그인 요청: {}", request.getEmail());

        // Service Layer 호출
        LoginResponseDto response = authService.login(request);

        // 표준 응답 포맷으로 래핑하여 반환
        return ResponseEntity.ok(
                ApiResponse.success(response, "로그인에 성공했습니다.")
        );
    }
}

