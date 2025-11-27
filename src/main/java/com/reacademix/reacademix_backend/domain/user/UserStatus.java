package com.reacademix.reacademix_backend.domain.user;

/**
 * 사용자 상태 Enum
 * MVP에서는 ACTIVE만 사용하지만, 향후 확장 가능
 */
public enum UserStatus {
    ACTIVE,     // 정상 사용 가능 (MVP 기본값)
    INACTIVE,   // 비활성화
    SUSPENDED   // 일시 정지
}

