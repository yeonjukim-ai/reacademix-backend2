package com.reacademix.reacademix_backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Spring Security 설정
 * PasswordEncoder Bean 등록
 */
@Configuration
public class SecurityConfig {

    /**
     * PasswordEncoder Bean 등록
     * bcrypt 알고리즘 사용 (salt rounds: 10)
     * @return PasswordEncoder BCryptPasswordEncoder 인스턴스
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);  // salt rounds: 10
    }
}

