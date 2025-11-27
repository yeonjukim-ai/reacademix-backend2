# 개인정보 암호화 저장 구현

- **Type**: Non-Functional
- **Key**: BE-SECURITY-001
- **REQ / Epic**: REQ-NF-016
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003

## 📌 Description

학생 및 학부모의 개인정보(이름, 이메일, 전화번호)를 암호화하여 저장하는 기능을 구현합니다.

## ✅ Acceptance Criteria

- [ ] 암호화 라이브러리 의존성 추가 (Jasypt 또는 Java Cryptography Extension)
- [ ] EncryptionService 클래스 구현
- [ ] 개인정보 암호화 메서드 구현
- [ ] 개인정보 복호화 메서드 구현
- [ ] 학생 이름 암호화 저장
- [ ] 학부모 이메일 암호화 저장
- [ ] 학부모 전화번호 암호화 저장
- [ ] 암호화 키 관리 (환경 변수 또는 키 관리 시스템)
- [ ] 암호화 실패 시 에러 반환
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- 구현 세부사항은 acceptance criteria 참조


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-12
- **Lane**: NFR
## 🔗 Traceability

- Related SRS: REQ-NF-016
- Related Epic: Security
