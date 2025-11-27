package com.reacademix.reacademix_backend.domain.user;

/**
 * 사용자 역할 Enum
 * MVP에서는 ADMIN만 사용하지만, 향후 확장 가능
 */
public enum UserRole {
    ADMIN,      // 관리자 (MVP 기본값)
    MANAGER,    // 관리자 (확장)
    STAFF       // 직원 (확장)
}

