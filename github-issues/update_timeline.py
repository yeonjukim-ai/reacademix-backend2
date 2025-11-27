#!/usr/bin/env python3
"""
Gantt 차트 정보를 GitHub Issue 파일에 Timeline 섹션으로 추가하는 스크립트
"""

import re
from pathlib import Path
from datetime import datetime

# 현재 스크립트 위치에서 경로 계산
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
GANTT_FILE = REPO_ROOT / "docs" / "DAG-gantt-backend.md"
ISSUE_INDEX_FILE = REPO_ROOT / "reacademix-backend" / "docs" / "issue-index-backend.md"
ISSUES_DIR = SCRIPT_DIR

def parse_gantt_table():
    """Gantt 차트 테이블에서 Task 정보 파싱"""
    tasks = {}
    
    print(f"Reading Gantt file: {GANTT_FILE}")
    with open(GANTT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 테이블 패턴 매칭
    pattern = r'\|\s+\*\*(BE-[A-Z0-9-]+)\*\*\s+\|\s+(.+?)\s+\|\s+(.+?)\s+\|\s+(\d{4}-\d{2}-\d{2})\s+\|\s+(\d{4}-\d{2}-\d{2})'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        task_id = match.group(1)
        title = match.group(2).strip()
        lane = match.group(3).strip()
        start_date = match.group(4)
        end_date = match.group(5)
        
        tasks[task_id] = {
            'title': title,
            'lane': lane,
            'start_date': start_date,
            'end_date': end_date
        }
        print(f"  Found: {task_id} - {title} ({start_date} ~ {end_date})")
    
    return tasks

def find_issue_file(task_key):
    """Task Key로 Issue 파일 찾기"""
    for issue_file in ISSUES_DIR.glob(f"{task_key}-*.md"):
        return issue_file
    return None

def update_issue_file(issue_file, start_date, end_date, lane):
    """Issue 파일에 Timeline 섹션 추가/업데이트"""
    with open(issue_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Timeline 섹션 생성
    timeline_section = f"""
## ⏱ 일정(Timeline)

- **Start**: {start_date}
- **End**: {end_date}
- **Lane**: {lane}
"""
    
    # 이미 Timeline 섹션이 있는지 확인
    if '## ⏱ 일정(Timeline)' in content or '## ⏱️ 일정(Timeline)' in content:
        # 기존 섹션 교체
        pattern = r'## ⏱[️]? 일정\(Timeline\).*?(?=\n## |\Z)'
        content = re.sub(pattern, timeline_section.strip(), content, flags=re.DOTALL)
        updated = True
    else:
        # Traceability 섹션 앞에 추가
        if '## 🔗 Traceability' in content:
            content = content.replace('## 🔗 Traceability', timeline_section + '\n## 🔗 Traceability')
            updated = True
        else:
            # 파일 끝에 추가
            content += timeline_section
            updated = True
    
    # 파일 저장
    with open(issue_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return updated

def main():
    print("="*80)
    print("Gantt 차트 정보를 GitHub Issue 파일에 동기화")
    print("="*80)
    print()
    
    # 1. Gantt 차트 파싱
    print("Step 1: Gantt 차트 파싱 중...")
    tasks = parse_gantt_table()
    print(f"✅ {len(tasks)}개의 Task 정보를 파싱했습니다.\n")
    
    # 2. Issue 파일 업데이트
    print("Step 2: Issue 파일 업데이트 중...")
    updated_files = []
    not_found = []
    
    for task_key, task_info in sorted(tasks.items()):
        issue_file = find_issue_file(task_key)
        if issue_file:
            update_issue_file(
                issue_file,
                task_info['start_date'],
                task_info['end_date'],
                task_info['lane']
            )
            updated_files.append({
                'task_key': task_key,
                'file': issue_file.name,
                'start_date': task_info['start_date'],
                'end_date': task_info['end_date'],
                'lane': task_info['lane']
            })
            print(f"  ✅ {task_key}: {issue_file.name}")
        else:
            not_found.append(task_key)
            print(f"  ⚠️  {task_key}: 파일을 찾을 수 없습니다")
    
    print(f"\n✅ {len(updated_files)}개의 Issue 파일을 업데이트했습니다.")
    if not_found:
        print(f"⚠️  {len(not_found)}개의 Task에 대한 파일을 찾을 수 없습니다.")
    
    print("\n" + "="*80)
    print("업데이트 완료!")
    print("="*80)
    print("\n다음 단계:")
    print("1. GitHub Issues 본문 업데이트를 위해 각 이슈를 수동으로 업데이트하거나")
    print("2. gh CLI를 사용하여 Issue 본문을 업데이트하세요.")
    print("\n업데이트된 파일 목록:")
    for item in updated_files:
        print(f"  - {item['task_key']}: {item['file']} ({item['start_date']} ~ {item['end_date']}, {item['lane']})")

if __name__ == '__main__':
    main()

