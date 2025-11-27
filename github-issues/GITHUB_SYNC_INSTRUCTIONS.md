# GitHub Issues 및 Projects 자동 반영 가이드

## 작업 완료 상태

✅ **Issue 파일 업데이트**: 모든 39개 Issue 파일에 Timeline 섹션이 추가되었습니다.

## GitHub에 반영하기

### 방법 1: PowerShell 스크립트 실행 (권장)

```powershell
cd reacademix-backend/github-issues
.\run_github_sync.ps1
```

이 스크립트는:
- 모든 Issue 본문을 업데이트합니다
- 모든 Issue를 `reacademix-backend` 프로젝트에 추가합니다

### 방법 2: 개별 명령어 실행

각 Issue에 대해 다음 명령어를 실행하세요:

```bash
# Issue 본문 업데이트
gh issue edit ISSUE_NUMBER --body-file "BE-XXX-XXX-파일명.md"

# Project 추가
gh issue edit ISSUE_NUMBER --add-project reacademix-backend
```

### 방법 3: Bash 스크립트 실행 (Linux/Mac)

```bash
cd reacademix-backend/github-issues
chmod +x gh_commands.sh
./gh_commands.sh
```

## 모든 Issue 목록 및 명령어

| Task ID | Issue # | 파일명 | 명령어 |
|---------|---------|--------|--------|
| BE-INFRA-001 | #16 | BE-INFRA-001-프로젝트-기본-설정-및-의존성-구성.md | `gh issue edit 16 --body-file "BE-INFRA-001-프로젝트-기본-설정-및-의존성-구성.md" --add-project reacademix-backend` |
| BE-INFRA-002 | #17 | BE-INFRA-002-데이터베이스-연결-설정-및-JPA-엔티티-기본-구조.md | `gh issue edit 17 --body-file "BE-INFRA-002-데이터베이스-연결-설정-및-JPA-엔티티-기본-구조.md" --add-project reacademix-backend` |
| BE-INFRA-003 | #18 | BE-INFRA-003-데이터베이스-스키마-생성-및-마이그레이션.md | `gh issue edit 18 --body-file "BE-INFRA-003-데이터베이스-스키마-생성-및-마이그레이션.md" --add-project reacademix-backend` |
| BE-COMMON-001 | #4 | BE-COMMON-001-전역-에러-핸들링-구현.md | `gh issue edit 4 --body-file "BE-COMMON-001-전역-에러-핸들링-구현.md" --add-project reacademix-backend` |
| BE-COMMON-002 | #5 | BE-COMMON-002-로깅-및-모니터링-설정.md | `gh issue edit 5 --body-file "BE-COMMON-002-로깅-및-모니터링-설정.md" --add-project reacademix-backend` |
| BE-COMMON-003 | #6 | BE-COMMON-003-API-문서화-Swagger-OpenAPI.md | `gh issue edit 6 --body-file "BE-COMMON-003-API-문서화-Swagger-OpenAPI.md" --add-project reacademix-backend` |
| BE-AUTH-001 | #1 | BE-AUTH-001-사용자-인증-API-구현-로그인.md | `gh issue edit 1 --body-file "BE-AUTH-001-사용자-인증-API-구현-로그인.md" --add-project reacademix-backend` |
| BE-AUTH-002 | #2 | BE-AUTH-002-JWT-토큰-검증-미들웨어-구현.md | `gh issue edit 2 --body-file "BE-AUTH-002-JWT-토큰-검증-미들웨어-구현.md" --add-project reacademix-backend` |
| BE-AUTH-003 | #3 | BE-AUTH-003-사용자-로그아웃-API-구현.md | `gh issue edit 3 --body-file "BE-AUTH-003-사용자-로그아웃-API-구현.md" --add-project reacademix-backend` |
| ... | ... | ... | ... |

(전체 목록은 `GANTT_SYNC_SUMMARY.md` 참조)

## ⚠️ 중요 참고사항

### GitHub Projects Date 필드 설정

GitHub Projects의 Date 필드(Start Date, Due Date)는 GitHub CLI로 **직접 설정할 수 없습니다**.

**설정 방법**:
1. **웹 UI 사용** (가장 간단):
   - GitHub Projects 페이지로 이동
   - 각 Issue의 Date 필드를 수동으로 설정
   - `GANTT_SYNC_SUMMARY.md` 파일의 Timeline 정보 참고

2. **GitHub Projects API 사용** (고급):
   - GitHub Projects API를 사용하여 Date 필드 설정
   - Node ID와 Field ID가 필요

**Date 정보**: 모든 Task의 Start/End 날짜는 각 Issue 본문의 `⏱ 일정(Timeline)` 섹션에 포함되어 있습니다.

## 확인 방법

동기화가 완료되면 다음을 확인하세요:

1. **GitHub Issues 페이지**: 각 Issue 본문에 Timeline 섹션이 포함되어 있는지 확인
2. **GitHub Projects 페이지**: 모든 Issue가 `reacademix-backend` 프로젝트에 추가되어 있는지 확인
3. **Date 필드**: Projects에서 각 Issue의 Start Date와 Due Date가 올바르게 설정되어 있는지 확인 (수동 설정 필요)

## 문제 해결

### GitHub CLI 인증 오류

```bash
gh auth login
```

### Project가 존재하지 않음

먼저 GitHub에서 `reacademix-backend` 프로젝트가 생성되어 있는지 확인하세요.

### Date 필드를 CLI로 설정하고 싶은 경우

GitHub Projects API를 사용해야 합니다. 자세한 내용은 [GitHub Projects API 문서](https://docs.github.com/en/graphql/reference/mutations#updateprojectv2itemfieldvalue)를 참조하세요.

