# GitHub Issues 및 Projects 자동 반영 실행 가이드

## 작업 완료 현황

✅ **모든 Issue 파일 업데이트**: 39개 파일에 Timeline 섹션 추가 완료  
⏳ **GitHub 반영**: 진행 중

## 실행 방법

### 방법 1: PowerShell 스크립트 실행 (권장)

```powershell
cd reacademix-backend/github-issues
.\AUTO_SYNC_TO_GITHUB.ps1
```

### 방법 2: Python 스크립트 실행

```bash
cd reacademix-backend/github-issues
python final_sync_to_github.py
```

### 방법 3: 개별 명령어 실행

아래 명령어들을 순서대로 실행하세요:

```bash
# Issue 본문 업데이트
gh issue edit ISSUE_NUMBER --body-file "BE-XXX-XXX-파일명.md"

# Project 추가
gh issue edit ISSUE_NUMBER --add-project reacademix-backend
```

## 모든 Issue별 명령어 목록

### Prerequisites Lane

```bash
gh issue edit 16 --body-file "BE-INFRA-001-프로젝트-기본-설정-및-의존성-구성.md" --add-project reacademix-backend
gh issue edit 17 --body-file "BE-INFRA-002-데이터베이스-연결-설정-및-JPA-엔티티-기본-구조.md" --add-project reacademix-backend
gh issue edit 18 --body-file "BE-INFRA-003-데이터베이스-스키마-생성-및-마이그레이션.md" --add-project reacademix-backend
gh issue edit 4 --body-file "BE-COMMON-001-전역-에러-핸들링-구현.md" --add-project reacademix-backend
gh issue edit 5 --body-file "BE-COMMON-002-로깅-및-모니터링-설정.md" --add-project reacademix-backend
gh issue edit 6 --body-file "BE-COMMON-003-API-문서화-Swagger-OpenAPI.md" --add-project reacademix-backend
```

### Backend Core Lane

```bash
gh issue edit 1 --body-file "BE-AUTH-001-사용자-인증-API-구현-로그인.md" --add-project reacademix-backend
gh issue edit 2 --body-file "BE-AUTH-002-JWT-토큰-검증-미들웨어-구현.md" --add-project reacademix-backend
gh issue edit 3 --body-file "BE-AUTH-003-사용자-로그아웃-API-구현.md" --add-project reacademix-backend
gh issue edit 38 --body-file "BE-STUDENT-001-학생-검색-API-구현.md" --add-project reacademix-backend
gh issue edit 39 --body-file "BE-STUDENT-002-학생-상세-정보-조회-API-구현.md" --add-project reacademix-backend
# ... (나머지 Backend Core 작업들)
```

(전체 목록은 `GANTT_SYNC_SUMMARY.md` 참조)

## ⚠️ 중요 참고사항

1. **Date 필드 설정**: GitHub Projects의 Date 필드는 CLI로 직접 설정할 수 없습니다.
   - 웹 UI에서 수동 설정 필요
   - 또는 GitHub Projects API 사용

2. **프로젝트 이름 확인**: `reacademix-backend` 프로젝트가 GitHub에 존재하는지 확인하세요.

3. **GitHub CLI 인증**: `gh auth status`로 인증 상태를 확인하세요.

## 확인 방법

동기화 완료 후 다음을 확인하세요:

1. GitHub Issues 페이지에서 각 Issue 본문에 Timeline 섹션 확인
2. GitHub Projects 페이지에서 모든 Issue가 프로젝트에 추가되었는지 확인
3. Projects에서 Date 필드가 올바르게 설정되었는지 확인 (수동 설정 필요)

