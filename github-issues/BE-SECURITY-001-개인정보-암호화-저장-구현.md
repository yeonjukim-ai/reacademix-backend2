# 개인정보 암호화 저장 구현

- **Type**: Non-Functional
- **Key**: BE-SECURITY-001
- **REQ / Epic**: REQ-NF-016
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생 및 학부모의 개인정보(이름, 이메일, 전화번호)를 AES-256으로 암호화하여 저장하는 기능을 구현합니다.

## ✅ Acceptance Criteria

### 암호화 구현
- [ ] AES-256 암호화 유틸리티 구현
- [ ] `EncryptionService` 클래스 생성
- [ ] 암호화/복호화 메서드 구현

### JPA Converter
- [ ] `EncryptedStringConverter` 구현
- [ ] Entity 필드에 `@Convert` 적용

### 키 관리
- [ ] 암호화 키 환경 변수로 관리
- [ ] 키 로테이션 고려

### 테스트
- [ ] 단위 테스트 작성
- [ ] 암호화/복호화 검증

---

## 💻 구현 코드

### application.properties

```properties
# Encryption (AES-256)
encryption.secret-key=${ENCRYPTION_SECRET_KEY:default-key-for-dev-only-32bytes!}
```

### EncryptionService.java

```java
package com.reacademix.reacademix_backend.security;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

@Slf4j
@Service
public class EncryptionService {

    private static final String ALGORITHM = "AES";
    private final SecretKeySpec secretKey;

    public EncryptionService(@Value("${encryption.secret-key}") String key) {
        byte[] keyBytes = key.getBytes(StandardCharsets.UTF_8);
        if (keyBytes.length != 32) {
            throw new IllegalArgumentException("AES-256 requires a 32-byte key");
        }
        this.secretKey = new SecretKeySpec(keyBytes, ALGORITHM);
    }

    /**
     * 문자열 암호화
     */
    public String encrypt(String plainText) {
        if (plainText == null || plainText.isEmpty()) {
            return plainText;
        }
        try {
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] encrypted = cipher.doFinal(plainText.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(encrypted);
        } catch (Exception e) {
            log.error("암호화 실패: {}", e.getMessage());
            throw new RuntimeException("암호화 처리 중 오류가 발생했습니다.", e);
        }
    }

    /**
     * 문자열 복호화
     */
    public String decrypt(String encryptedText) {
        if (encryptedText == null || encryptedText.isEmpty()) {
            return encryptedText;
        }
        try {
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, secretKey);
            byte[] decoded = Base64.getDecoder().decode(encryptedText);
            byte[] decrypted = cipher.doFinal(decoded);
            return new String(decrypted, StandardCharsets.UTF_8);
        } catch (Exception e) {
            log.error("복호화 실패: {}", e.getMessage());
            throw new RuntimeException("복호화 처리 중 오류가 발생했습니다.", e);
        }
    }
}
```

### EncryptedStringConverter.java

```java
package com.reacademix.reacademix_backend.security;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@Converter
@RequiredArgsConstructor
public class EncryptedStringConverter implements AttributeConverter<String, String> {

    private final EncryptionService encryptionService;

    @Override
    public String convertToDatabaseColumn(String attribute) {
        return encryptionService.encrypt(attribute);
    }

    @Override
    public String convertToEntityAttribute(String dbData) {
        return encryptionService.decrypt(dbData);
    }
}
```

### Student.java (적용 예시)

```java
@Entity
@Table(name = "students")
public class Student extends BaseTimeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "name", nullable = false, length = 255)
    private String name;  // 암호화 저장

    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "parent_email", length = 255)
    private String parentEmail;  // 암호화 저장

    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "parent_phone", length = 255)
    private String parentPhone;  // 암호화 저장

    @Column(name = "student_code", nullable = false, unique = true)
    private String studentCode;  // 암호화 불필요
}
```

---

## 📝 구현 체크리스트

- [ ] `EncryptionService` 구현
- [ ] `EncryptedStringConverter` 구현
- [ ] Entity 필드에 적용
- [ ] 환경 변수 설정
- [ ] 테스트 작성

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-12
- **Lane**: NFR

## 🔗 Traceability

- Related SRS: REQ-NF-016
- Related Epic: Security
