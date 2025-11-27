package com.reacademix.reacademix_backend.controller;

import com.reacademix.reacademix_backend.dto.request.UserSignupRequest;
import com.reacademix.reacademix_backend.dto.response.UserResponse;
import com.reacademix.reacademix_backend.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * User 관련 REST API Controller
 */
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * 회원가입 API
     * @param request 회원가입 요청 DTO
     * @return ResponseEntity<UserResponse> 회원가입 응답 (201 Created)
     */
    @PostMapping
    public ResponseEntity<UserResponse> signup(@Valid @RequestBody UserSignupRequest request) {
        UserResponse response = userService.signup(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}

