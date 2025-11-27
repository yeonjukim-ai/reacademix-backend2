# 데이터 통합 서비스 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-004
- **REQ / Epic**: REQ-FUNC-019
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INTEGRATION-002, BE-INFRA-003

## 📌 Description

여러 시스템에서 수집된 데이터를 학생 ID 기준으로 통합하여 데이터베이스에 저장하는 서비스를 구현합니다.

## ✅ Acceptance Criteria

- [ ] DataIntegrationService.integrateData() 메서드 구현
- [ ] 학생 ID 기준 데이터 그룹핑
- [ ] 배치 쓰기 사용 (JPA Batch Insert)
- [ ] attendance 테이블에 출석 데이터 저장
- [ ] study_time 테이블에 학습 시간 데이터 저장
- [ ] mock_exam 테이블에 모의고사 성적 데이터 저장
- [ ] payment 테이블에 결제 데이터 저장 (선택)
- [ ] 통합 완료 상태 반환
- [ ] 저장된 데이터 개수 반환
- [ ] 학생 ID 없을 시 해당 데이터 건너뛰기
- [ ] 배치 쓰기 실패 시 부분 실패 처리
- [ ] 중복 데이터 업데이트 또는 건너뛰기
- [ ] 데이터 통합 정확도 99% 이상 (REQ-NF-007)
- [ ] 처리 시간 학원당 평균 2분 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- Repository 레이어
- 관련 테이블: attendance, study_time, mock_exam


## ⏱ 일정(Timeline)

- **Start**: 2025-12-08
- **End**: 2025-12-12
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-019
- Related Epic: Data Integration
