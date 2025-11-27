package com.reacademix.reacademix_backend.repository;

import com.reacademix.reacademix_backend.domain.user.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * User 엔티티를 위한 Repository 인터페이스
 * Spring Data JPA를 사용하여 데이터베이스 접근
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * 이메일로 사용자 조회
     * @param email 사용자 이메일 (소문자로 정규화되어 저장됨)
     * @return Optional<User> 사용자 정보 (없으면 empty)
     */
    Optional<User> findByEmail(String email);

    /**
     * 이메일 존재 여부 확인 (성능 최적화용)
     * @param email 사용자 이메일
     * @return boolean 이메일 존재 여부
     */
    boolean existsByEmail(String email);
}

