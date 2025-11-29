package com.reacademix.reacademix_backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.annotation.web.configurers.HeadersConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Spring Security 설정
 * JWT 기반 인증을 위한 보안 설정 및 PasswordEncoder Bean 등록
 * 
 * @author Backend Team
 * @version 1.0
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * PasswordEncoder Bean 등록
     * bcrypt 알고리즘 사용 (salt rounds: 10)
     * 
     * @return PasswordEncoder BCryptPasswordEncoder 인스턴스
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);  // salt rounds: 10
    }

    /**
     * Spring Security 필터 체인 설정
     * - CSRF 비활성화 (JWT 사용으로 불필요)
     * - 세션 관리 비활성화 (Stateless)
     * - 인증 없이 접근 가능한 엔드포인트 설정
     * 
     * @param http HttpSecurity 객체
     * @return SecurityFilterChain
     * @throws Exception 설정 오류 시
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // CSRF 비활성화 (REST API + JWT 사용으로 불필요)
            .csrf(AbstractHttpConfigurer::disable)
            
            // H2 Console iframe 허용 (개발용)
            .headers(headers -> headers
                .frameOptions(HeadersConfigurer.FrameOptionsConfig::sameOrigin)
            )
            
            // 세션 관리 비활성화 (JWT 기반 Stateless 인증)
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            
            // 요청별 접근 권한 설정
            .authorizeHttpRequests(auth -> auth
                // 인증 없이 접근 가능한 엔드포인트
                .requestMatchers("/api/v1/auth/**").permitAll()  // 로그인, 회원가입 등
                .requestMatchers("/h2-console/**").permitAll()   // H2 Console (개발용)
                .requestMatchers("/swagger-ui/**").permitAll()   // Swagger UI
                .requestMatchers("/v3/api-docs/**").permitAll()  // OpenAPI 문서
                .requestMatchers("/actuator/health").permitAll() // Health Check
                // 그 외 모든 요청은 인증 필요
                .anyRequest().authenticated()
            );

        return http.build();
    }
}
