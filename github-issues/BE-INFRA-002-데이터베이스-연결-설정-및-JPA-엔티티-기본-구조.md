# 데이터베이스 연결 설정 및 JPA 엔티티 기본 구조

- **Type**: Infrastructure
- **Key**: BE-INFRA-002
- **REQ / Epic**: Infrastructure Setup
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-001

## 📌 Description

PostgreSQL 또는 MySQL 데이터베이스 연결을 설정하고, JPA 엔티티의 기본 구조를 생성합니다. application.properties에 DB 연결 정보를 설정하고, 기본 엔티티 클래스들을 생성합니다.

## ✅ Acceptance Criteria

- [ ] application.properties에 DB 연결 정보 설정
- [ ] JPA 설정 (dialect, ddl-auto 등) 구성
- [ ] 기본 엔티티 클래스 생성 (User, Student, Attendance, StudyTime, MockExam, Assignment, Report, ReportDelivery)
- [ ] BaseEntity 클래스 생성 (createdAt, updatedAt 공통 필드)
- [ ] 데이터베이스 연결 테스트 성공

## 🧩 Technical Notes

- Repository 레이어
- 관련 엔티티: User, Student, Attendance, StudyTime, MockExam, Assignment, Report, ReportDelivery

## ⏱ 일정(Timeline)

- **Start**: 2025-11-30
- **End**: 2025-12-03
- **Lane**: Prerequisites
## 🔗 Traceability

- Related SRS: N/A
- Related Epic: Infrastructure Setup
