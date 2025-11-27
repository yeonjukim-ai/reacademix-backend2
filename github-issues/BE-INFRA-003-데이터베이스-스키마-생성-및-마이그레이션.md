# 데이터베이스 스키마 생성 및 마이그레이션

- **Type**: Infrastructure
- **Key**: BE-INFRA-003
- **REQ / Epic**: Infrastructure Setup
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-002

## 📌 Description

SRS 문서의 데이터 모델을 기반으로 데이터베이스 스키마를 생성합니다. Flyway 또는 Liquibase를 사용하여 마이그레이션 스크립트를 작성하고 실행합니다.

## ✅ Acceptance Criteria

- [ ] Flyway 또는 Liquibase 의존성 추가
- [ ] users 테이블 생성 스크립트 작성
- [ ] students 테이블 생성 스크립트 작성
- [ ] attendance 테이블 생성 스크립트 작성
- [ ] study_time 테이블 생성 스크립트 작성
- [ ] mock_exam 테이블 생성 스크립트 작성
- [ ] assignments 테이블 생성 스크립트 작성
- [ ] reports 테이블 생성 스크립트 작성
- [ ] report_delivery 테이블 생성 스크립트 작성
- [ ] 필요한 인덱스 생성 스크립트 작성
- [ ] 마이그레이션 실행 성공

## 🧩 Technical Notes

- Repository 레이어
- 관련 테이블: users, students, attendance, study_time, mock_exam, assignments, reports, report_delivery

## ⏱ 일정(Timeline)

- **Start**: 2025-12-04
- **End**: 2025-12-07
- **Lane**: Prerequisites
## 🔗 Traceability

- Related SRS: N/A
- Related Epic: Infrastructure Setup
