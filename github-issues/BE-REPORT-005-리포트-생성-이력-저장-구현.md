# 리포트 생성 이력 저장 구현

- **Type**: Functional
- **Key**: BE-REPORT-005
- **REQ / Epic**: REQ-FUNC-013
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003, BE-REPORT-003

## 📌 Description

리포트 생성 이벤트를 Firestore 또는 데이터베이스에 로그로 저장하는 기능을 구현합니다.

## ✅ Acceptance Criteria

- [ ] ReportHistoryService.saveReportHistory() 메서드 구현
- [ ] 리포트 ID, 학생 ID, 생성 시간, 리포트 유형, 다운로드 여부 저장
- [ ] reports 테이블에 리포트 생성 이력 저장
- [ ] 저장 완료 확인
- [ ] Firestore 저장 실패 시 에러 반환
- [ ] 필수 필드 누락 시 검증 에러 반환
- [ ] 저장 시간 1초 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Repository 레이어
- 관련 엔티티: Report
- 관련 테이블: reports


## ⏱ 일정(Timeline)

- **Start**: 2025-12-25
- **End**: 2025-12-26
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-013
- Related Epic: Report Generation
