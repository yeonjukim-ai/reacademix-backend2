# Gantt 차트 정보 GitHub Issues 동기화 상태

## ✅ 완료된 작업

1. **Task 정보 파싱**: Gantt 차트에서 39개 Task의 정보를 추출했습니다.
2. **요약 문서 생성**: `GANTT_SYNC_SUMMARY.md` 파일을 생성했습니다.
3. **핵심 파일 업데이트**: 몇 개의 핵심 Issue 파일에 Timeline 섹션을 추가했습니다.
4. **gh CLI 명령어 스크립트**: `gh_commands.sh` 파일을 생성했습니다.

## 🔄 진행 중인 작업

### Issue 파일 업데이트

나머지 Issue 파일들에 Timeline 섹션을 추가해야 합니다.

**스크립트 실행 방법:**
```bash
cd reacademix-backend/github-issues
python batch_update_timeline.py
```

또는 수동으로 각 파일에 다음 형식의 Timeline 섹션을 추가:
```markdown
## ⏱ 일정(Timeline)

- **Start**: YYYY-MM-DD
- **End**: YYYY-MM-DD
- **Lane**: Lane Name
```

## 📋 Task별 Timeline 정보

모든 Task의 Timeline 정보는 `GANTT_SYNC_SUMMARY.md` 파일에 정리되어 있습니다.

## 🔧 다음 단계

1. **모든 Issue 파일 업데이트**
   - `batch_update_timeline.py` 스크립트 실행
   - 또는 수동으로 각 파일 업데이트

2. **GitHub Issues 본문 업데이트**
   - 각 Issue 파일을 읽어서 GitHub에 업데이트
   - 또는 `gh issue edit` 명령어 사용

3. **GitHub Projects에 반영**
   - `gh_commands.sh` 스크립트 실행
   - 또는 개별 `gh issue edit` 명령어 실행

## ⚠️ 주의사항

1. GitHub Projects의 Date 필드는 CLI로 직접 설정할 수 없습니다.
   - 웹 UI에서 수동으로 설정하거나
   - GitHub Projects API를 사용해야 합니다.

2. Issue 본문은 파일만 업데이트하면 자동으로 반영되지 않습니다.
   - 별도로 GitHub에 업데이트해야 합니다.

