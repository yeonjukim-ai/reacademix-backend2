package com.reacademix.reacademix_backend.security;

import com.reacademix.reacademix_backend.domain.user.User;
import com.reacademix.reacademix_backend.exception.AuthException;
import com.reacademix.reacademix_backend.exception.ErrorCode;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT 토큰 생성 및 검증을 담당하는 Provider 클래스
 * 
 * @author Backend Team
 * @version 1.0
 */
@Slf4j
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String secretKeyString;

    @Value("${jwt.expiration}")
    private long expirationTime;

    private SecretKey secretKey;

    /**
     * 초기화 메서드
     * secretKeyString을 SecretKey 객체로 변환
     */
    @PostConstruct
    public void init() {
        this.secretKey = Keys.hmacShaKeyFor(secretKeyString.getBytes(StandardCharsets.UTF_8));
    }

    /**
     * 사용자 정보를 기반으로 JWT 토큰 생성
     * 
     * @param user 사용자 엔티티
     * @return JWT 토큰 문자열
     * @throws AuthException 토큰 생성 실패 시
     */
    public String generateToken(User user) {
        try {
            Date now = new Date();
            Date expiry = new Date(now.getTime() + expirationTime);

            return Jwts.builder()
                    .subject(user.getId().toString())
                    .claim("email", user.getEmail())
                    .claim("role", user.getRole().name())
                    .issuedAt(now)
                    .expiration(expiry)
                    .signWith(secretKey)
                    .compact();
        } catch (Exception e) {
            log.error("JWT 토큰 생성 실패: {}", e.getMessage(), e);
            throw new AuthException(ErrorCode.SYSTEM_003, e);
        }
    }

    /**
     * JWT 토큰에서 사용자 ID 추출
     * 
     * @param token JWT 토큰
     * @return 사용자 ID
     * @throws AuthException 토큰이 유효하지 않거나 만료된 경우
     */
    public Long getUserIdFromToken(String token) {
        Claims claims = parseToken(token);
        return Long.parseLong(claims.getSubject());
    }

    /**
     * JWT 토큰에서 이메일 추출
     * 
     * @param token JWT 토큰
     * @return 사용자 이메일
     * @throws AuthException 토큰이 유효하지 않거나 만료된 경우
     */
    public String getEmailFromToken(String token) {
        Claims claims = parseToken(token);
        return claims.get("email", String.class);
    }

    /**
     * JWT 토큰 유효성 검증
     * 
     * @param token JWT 토큰
     * @return 유효하면 true
     * @throws AuthException 토큰이 만료되었거나 유효하지 않은 경우
     */
    public boolean validateToken(String token) {
        try {
            parseToken(token);
            return true;
        } catch (AuthException e) {
            throw e;
        }
    }

    /**
     * JWT 토큰 파싱 및 Claims 반환
     * 
     * @param token JWT 토큰
     * @return Claims 객체
     * @throws AuthException 토큰이 만료되었거나 유효하지 않은 경우
     */
    private Claims parseToken(String token) {
        try {
            return Jwts.parser()
                    .verifyWith(secretKey)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
        } catch (ExpiredJwtException e) {
            log.warn("JWT 토큰 만료: {}", e.getMessage());
            throw new AuthException(ErrorCode.AUTH_005);
        } catch (JwtException e) {
            log.warn("유효하지 않은 JWT 토큰: {}", e.getMessage());
            throw new AuthException(ErrorCode.AUTH_006);
        }
    }

    /**
     * 토큰 만료 시간(초) 반환
     * 
     * @return 만료 시간(초 단위)
     */
    public long getExpirationTimeInSeconds() {
        return expirationTime / 1000;
    }
}

