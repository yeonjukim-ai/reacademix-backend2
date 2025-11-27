# Gantt 차트 정보 GitHub Issues 동기화 결과

## 작업 개요

Gantt 차트(`docs/DAG-gantt-backend.md`)의 일정 정보를 모든 GitHub Issue 파일에 반영했습니다.

## 업데이트된 Issue 목록 (39개)

### Prerequisites Lane (6개)

| Task ID | Issue # | 파일명 | Start | End | Lane |
|---------|---------|--------|-------|-----|------|
| BE-INFRA-001 | #16 | BE-INFRA-001-프로젝트-기본-설정-및-의존성-구성.md | 2025-11-27 | 2025-11-29 | Prerequisites |
| BE-INFRA-002 | #17 | BE-INFRA-002-데이터베이스-연결-설정-및-JPA-엔티티-기본-구조.md | 2025-11-30 | 2025-12-03 | Prerequisites |
| BE-INFRA-003 | #18 | BE-INFRA-003-데이터베이스-스키마-생성-및-마이그레이션.md | 2025-12-04 | 2025-12-07 | Prerequisites |
| BE-COMMON-001 | #4 | BE-COMMON-001-전역-에러-핸들링-구현.md | 2025-11-30 | 2025-12-02 | Prerequisites |
| BE-COMMON-002 | #5 | BE-COMMON-002-로깅-및-모니터링-설정.md | 2025-11-30 | 2025-12-03 | Prerequisites |
| BE-COMMON-003 | #6 | BE-COMMON-003-API-문서화-Swagger-OpenAPI.md | 2025-11-30 | 2025-12-02 | Prerequisites |

### Backend Core Lane (23개)

| Task ID | Issue # | 파일명 | Start | End | Lane |
|---------|---------|--------|-------|-----|------|
| BE-AUTH-001 | #1 | BE-AUTH-001-사용자-인증-API-구현-로그인.md | 2025-12-08 | 2025-12-11 | Backend Core |
| BE-AUTH-002 | #2 | BE-AUTH-002-JWT-토큰-검증-미들웨어-구현.md | 2025-12-12 | 2025-12-14 | Backend Core |
| BE-AUTH-003 | #3 | BE-AUTH-003-사용자-로그아웃-API-구현.md | 2025-12-15 | 2025-12-16 | Backend Core |
| BE-STUDENT-001 | #38 | BE-STUDENT-001-학생-검색-API-구현.md | 2025-12-15 | 2025-12-17 | Backend Core |
| BE-STUDENT-002 | #39 | BE-STUDENT-002-학생-상세-정보-조회-API-구현.md | 2025-12-15 | 2025-12-17 | Backend Core |
| BE-INTEGRATION-001 | #20 | BE-INTEGRATION-001-파일-업로드-처리-서비스-구현.md | 2025-11-30 | 2025-12-04 | Backend Core |
| BE-INTEGRATION-002 | #21 | BE-INTEGRATION-002-데이터-검증-서비스-구현.md | 2025-11-30 | 2025-12-03 | Backend Core |
| BE-INTEGRATION-003 | #22 | BE-INTEGRATION-003-파일-업로드-데이터-수집-API-구현.md | 2025-12-15 | 2025-12-18 | Backend Core |
| BE-INTEGRATION-004 | #23 | BE-INTEGRATION-004-데이터-통합-서비스-구현.md | 2025-12-08 | 2025-12-12 | Backend Core |
| BE-INTEGRATION-005 | #24 | BE-INTEGRATION-005-수동-데이터-입력-API-구현.md | 2025-12-13 | 2025-12-15 | Backend Core |
| BE-INTEGRATION-006 | #25 | BE-INTEGRATION-006-통합-대시보드-데이터-조회-서비스-구현.md | 2025-12-08 | 2025-12-11 | Backend Core |
| BE-INTEGRATION-007 | #26 | BE-INTEGRATION-007-통합-대시보드-조회-API-구현.md | 2025-12-15 | 2025-12-17 | Backend Core |
| BE-REPORT-001 | #30 | BE-REPORT-001-리포트-템플릿-기본-설정-및-렌더링.md | 2025-11-30 | 2025-12-03 | Backend Core |
| BE-REPORT-002 | #31 | BE-REPORT-002-리포트-PDF-생성-서비스-구현.md | 2025-12-04 | 2025-12-08 | Backend Core |
| BE-REPORT-003 | #32 | BE-REPORT-003-리포트-생성-요청-API-구현.md | 2025-12-19 | 2025-12-24 | Backend Core |
| BE-REPORT-004 | #33 | BE-REPORT-004-리포트-생성-시간-제한-및-모니터링-구현.md | 2025-12-25 | 2025-12-27 | Backend Core |
| BE-REPORT-005 | #34 | BE-REPORT-005-리포트-생성-이력-저장-구현.md | 2025-12-25 | 2025-12-26 | Backend Core |
| BE-REPORT-006 | #35 | BE-REPORT-006-리포트-다운로드-API-구현.md | 2025-12-25 | 2025-12-27 | Backend Core |
| BE-REPORT-007 | #36 | BE-REPORT-007-리포트-생성-이력-조회-API-구현.md | 2025-12-27 | 2025-12-29 | Backend Core |
| BE-EMAIL-001 | #14 | BE-EMAIL-001-이메일-전송-서비스-구현.md | 2025-12-09 | 2025-12-12 | Backend Core |
| BE-EMAIL-002 | #15 | BE-EMAIL-002-수동-리포트-이메일-전송-API-구현.md | 2025-12-25 | 2025-12-28 | Backend Core |
| BE-DELIVERY-001 | #12 | BE-DELIVERY-001-리포트-전송-이력-저장-구현.md | 2025-12-08 | 2025-12-09 | Backend Core |
| BE-DELIVERY-002 | #13 | BE-DELIVERY-002-리포트-전송-이력-조회-API-구현.md | 2025-12-15 | 2025-12-17 | Backend Core |

### AI Engine Lane (1개)

| Task ID | Issue # | 파일명 | Start | End | Lane |
|---------|---------|--------|-------|-----|------|
| BE-INSIGHT-001 | #19 | BE-INSIGHT-001-인사이트-자동-생성-서비스-구현.md | 2025-12-12 | 2025-12-16 | AI Engine |

### Financial Lane (5개)

| Task ID | Issue # | 파일명 | Start | End | Lane |
|---------|---------|--------|-------|-----|------|
| BE-DATA-001 | #7 | BE-DATA-001-출석-데이터-조회-서비스-구현.md | 2025-12-08 | 2025-12-11 | Financial |
| BE-DATA-002 | #8 | BE-DATA-002-학습-시간-데이터-조회-서비스-구현.md | 2025-12-08 | 2025-12-11 | Financial |
| BE-DATA-003 | #9 | BE-DATA-003-모의고사-성적-데이터-조회-서비스-구현.md | 2025-12-08 | 2025-12-11 | Financial |
| BE-DATA-004 | #10 | BE-DATA-004-과제-완료도-데이터-조회-서비스-구현.md | 2025-12-08 | 2025-12-11 | Financial |
| BE-DATA-005 | #11 | BE-DATA-005-반-평균-데이터-계산-서비스-구현.md | 2025-12-08 | 2025-12-10 | Financial |

### NFR Lane (4개)

| Task ID | Issue # | 파일명 | Start | End | Lane |
|---------|---------|--------|-------|-----|------|
| BE-SECURITY-001 | #37 | BE-SECURITY-001-개인정보-암호화-저장-구현.md | 2025-12-08 | 2025-12-12 | NFR |
| BE-PERF-001 | #27 | BE-PERF-001-리포트-생성-성능-최적화.md | 2025-12-25 | 2025-12-29 | NFR |
| BE-PERF-002 | #28 | BE-PERF-002-동시-리포트-생성-처리-구현.md | 2025-12-25 | 2025-12-29 | NFR |
| BE-PERF-003 | #29 | BE-PERF-003-API-응답-시간-최적화.md | 2025-12-04 | 2025-12-08 | NFR |

## 추가된 Timeline 섹션 형식

각 Issue 파일에 다음 형식의 Timeline 섹션이 추가되었습니다:

```markdown
## ⏱ 일정(Timeline)

- **Start**: YYYY-MM-DD
- **End**: YYYY-MM-DD
- **Lane**: Lane Name
```

## 다음 단계

### 1. GitHub Issues 본문 업데이트

Issue 파일은 업데이트되었지만, 실제 GitHub Issues 본문은 아직 업데이트되지 않았습니다. 
다음 중 하나의 방법으로 업데이트할 수 있습니다:

- **방법 1**: 각 Issue 파일을 읽어서 GitHub에 직접 업데이트
- **방법 2**: `gh issue edit` 명령어로 본문 업데이트

### 2. GitHub Projects에 반영

다음 명령어들을 실행하여 GitHub Projects에 정보를 반영하세요:

```bash
# Project 추가 (모든 Issue)
gh issue edit ISSUE_NUMBER --add-project reacademix-backend

# 예시
gh issue edit 1 --add-project reacademix-backend
gh issue edit 2 --add-project reacademix-backend
# ... (모든 39개 Issue에 대해 반복)
```

**참고**: GitHub Projects의 Date 필드(Start Date, Due Date)는 GitHub CLI로 직접 설정할 수 없습니다.
- 웹 UI에서 수동으로 설정하거나
- GitHub Projects API를 사용해야 합니다.

### 3. Status 결정

현재 날짜(2025-01-27) 기준으로:

- **Backlog**: 시작일이 아직 오지 않은 작업
- **In Progress**: 현재 작업 기간에 해당하는 작업
- **Done**: 작업 기간이 이미 지난 작업 (모두 Backlog 상태, 아직 시작되지 않음)

## 실행할 gh CLI 명령어 목록

모든 Issue에 Project를 추가하는 명령어는 `gh_commands.sh` 파일에 정리되어 있습니다.

실행 방법:
```bash
cd reacademix-backend/github-issues
chmod +x gh_commands.sh
./gh_commands.sh
```

또는 개별적으로:
```bash
gh issue edit 1 --add-project reacademix-backend
gh issue edit 2 --add-project reacademix-backend
# ... (모든 Issue에 대해)
```

## 참고사항

1. **Date 필드 설정**: GitHub Projects의 Date 필드는 CLI로 직접 설정할 수 없으므로, 웹 UI에서 수동으로 설정하거나 Projects API를 사용해야 합니다.

2. **Issue 본문 업데이트**: Issue 파일은 업데이트되었지만, GitHub의 실제 Issue 본문은 별도로 업데이트해야 합니다.

3. **Milestone 설정**: 필요시 Milestone을 추가할 수 있습니다:
   ```bash
   gh issue edit ISSUE_NUMBER --milestone "Milestone Name"
   ```

