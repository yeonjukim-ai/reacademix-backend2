# GitHub Projects Roadmap 설정 가이드

**프로젝트**: reacademix-backend2 (프로젝트 번호: 5)  
**URL**: https://github.com/users/yeonjukim-ai/projects/5

---

## 🎯 목표

GitHub Projects의 Roadmap 뷰에서 Gantt 차트 형식으로 이슈 일정을 시각화합니다.

---

## 1단계: Date 필드 생성 (필수)

### 웹 UI에서 필드 생성

1. **프로젝트 페이지로 이동**
   - https://github.com/users/yeonjukim-ai/projects/5

2. **필드 추가**
   - 프로젝트 페이지 우측 상단의 **"+"** 버튼 클릭
   - 또는 프로젝트 설정에서 "Fields" 섹션으로 이동

3. **Date 필드 생성**
   - **필드 타입**: `Date` 선택
   - **필드 이름**: `Start date` (또는 `시작일`)
   - **생성** 클릭

4. **End Date 필드 생성** (선택사항)
   - **필드 타입**: `Date` 선택
   - **필드 이름**: `End date` (또는 `종료일`)
   - **생성** 클릭

**참고**: Start date만 있어도 Roadmap에서 표시됩니다. End date는 선택사항입니다.

---

## 2단계: 날짜 자동 설정 스크립트 실행

Date 필드를 생성한 후 다음 스크립트를 실행합니다:

```powershell
cd github-issues
python set_roadmap_dates.py
```

이 스크립트는:
- Execution Plan 문서의 일정을 기반으로 각 이슈에 날짜를 자동 설정합니다
- 기준일: 2025-01-27 (프로젝트 시작일)
- 각 이슈의 Day 범위를 실제 날짜로 변환합니다

---

## 3단계: Roadmap 뷰 확인

1. **프로젝트 페이지에서 "Roadmap" 탭 선택**
   - https://github.com/users/yeonjukim-ai/projects/5

2. **Gantt 차트 확인**
   - 각 이슈가 타임라인에 표시됩니다
   - 시작일과 종료일이 바 형태로 표시됩니다

---

## 일정 정보 (참고)

### Phase 1: 인프라 및 인증 (Week 1-2)
- **BE-INFRA-001**: 2025-01-27 ~ 2025-01-29 (Day 1-3)
- **BE-INFRA-002**: 2025-01-30 ~ 2025-02-01 (Day 4-6)
- **BE-INFRA-003**: 2025-02-02 ~ 2025-02-04 (Day 7-9)
- **BE-AUTH-001**: 2025-02-05 ~ 2025-02-07 (Day 10-12)
- **BE-AUTH-002**: 2025-02-08 ~ 2025-02-09 (Day 13-14)
- **BE-AUTH-003**: 2025-02-10 (Day 15)

### Phase 2: 핵심 기능 (Week 3-5)
- **BE-STUDENT-001~002**: 2025-02-11 ~ 2025-02-12 (Day 16-17)
- **BE-INTEGRATION-001~007**: 2025-01-28 ~ 2025-02-17 (Day 11-22)

### Phase 3: 리포트 생성 (Week 6-9)
- **BE-DATA-001~005**: 2025-02-18 ~ 2025-02-20 (Day 23-25)
- **BE-REPORT-003**: 2025-02-24 ~ 2025-02-28 (Day 29-33)

### Phase 4: 전송 및 비기능 (Week 10-11)
- **BE-EMAIL-001~002**: 2025-03-03 ~ 2025-03-05 (Day 38-42)
- **BE-PERF-001~003**: 2025-03-10 ~ 2025-03-12 (Day 43-45)

---

## 문제 해결

### Date 필드를 찾을 수 없음

**해결**: GitHub Projects 웹 UI에서 Date 필드를 먼저 생성해야 합니다.

### 권한 오류

**해결**: 
```bash
gh auth refresh -s read:project,write:project
```

### 날짜가 표시되지 않음

**확인 사항**:
1. Date 필드가 프로젝트에 생성되었는지 확인
2. 필드 이름이 정확한지 확인 (대소문자 구분)
3. 스크립트가 성공적으로 실행되었는지 확인

---

## 수동 설정 방법

스크립트가 작동하지 않는 경우, 웹 UI에서 수동으로 설정할 수 있습니다:

1. 프로젝트 페이지 → 각 이슈 클릭
2. "Start date" 필드에 날짜 입력
3. "End date" 필드에 날짜 입력 (선택사항)

---

**작성일**: 2025-01-27

