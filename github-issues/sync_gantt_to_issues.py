#!/usr/bin/env python3
"""
Gantt 차트 정보를 GitHub Issues와 Project에 동기화하는 스크립트

이 스크립트는:
1. DAG-gantt-backend.md에서 Task 정보를 파싱
2. 각 GitHub Issue 파일에 Timeline 섹션 추가/업데이트
3. gh CLI를 사용하여 GitHub Issues와 Project에 날짜 정보 반영
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

# 작업 디렉토리 설정
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
GANTT_FILE = REPO_ROOT / "docs" / "DAG-gantt-backend.md"
ISSUE_INDEX_FILE = REPO_ROOT / "reacademix-backend" / "docs" / "issue-index-backend.md"
ISSUES_DIR = SCRIPT_DIR

def parse_gantt_table() -> Dict[str, Dict[str, str]]:
    """Gantt 차트 테이블에서 Task 정보 파싱"""
    tasks = {}
    
    with open(GANTT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 테이블 찾기
    table_pattern = r'\| \*\*(BE-[A-Z0-9-]+)\*\* \| (.+?) \| (.+?) \| (\d{4}-\d{2}-\d{2}) \| (\d{4}-\d{2}-\d{2})'
    matches = re.finditer(table_pattern, content)
    
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
    
    return tasks

def parse_issue_index() -> Dict[str, int]:
    """Issue Index에서 Task Key와 Issue # 매핑 파싱"""
    mapping = {}
    
    with open(ISSUE_INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 테이블에서 매핑 찾기
    pattern = r'\| (BE-[A-Z0-9-]+) \| #(\d+) \|'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        task_key = match.group(1)
        issue_num = int(match.group(2))
        mapping[task_key] = issue_num
    
    return mapping

def normalize_lane_name(lane: str) -> str:
    """Lane 이름 정규화"""
    lane_mapping = {
        'Prerequisites': 'Prerequisites',
        'Backend Core': 'Backend Core',
        'AI Engine': 'AI Engine',
        'Financial': 'Financial',
        'NFR': 'NFR'
    }
    return lane_mapping.get(lane, lane)

def determine_status(start_date: str, end_date: str, current_date: Optional[str] = None) -> str:
    """날짜를 기반으로 Status 결정"""
    if current_date is None:
        current_date = datetime.now().strftime('%Y-%m-%d')
    
    if current_date < start_date:
        return "Backlog"
    elif start_date <= current_date <= end_date:
        return "In Progress"
    else:
        return "Done"

def update_issue_file(issue_file: Path, start_date: str, end_date: str, lane: str) -> bool:
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
    else:
        # Traceability 섹션 앞에 추가
        if '## 🔗 Traceability' in content:
            content = content.replace('## 🔗 Traceability', timeline_section + '\n## 🔗 Traceability')
        else:
            # 파일 끝에 추가
            content += timeline_section
    
    # 파일 저장
    with open(issue_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def find_issue_file(task_key: str) -> Optional[Path]:
    """Task Key로 Issue 파일 찾기"""
    # 파일명 패턴: BE-XXX-XXX-제목.md
    pattern = task_key.replace('-', '-') + '-*.md'
    
    for issue_file in ISSUES_DIR.glob(f"{task_key}-*.md"):
        return issue_file
    
    return None

def run_gh_command(cmd: list, description: str) -> Tuple[bool, str]:
    """gh CLI 명령어 실행"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def sync_to_github(tasks: Dict[str, Dict], mapping: Dict[str, int], current_date: str):
    """GitHub Issues와 Project에 정보 동기화"""
    commands_executed = []
    issues_updated = []
    
    for task_key, task_info in tasks.items():
        if task_key not in mapping:
            print(f"⚠️  Warning: {task_key}에 해당하는 Issue #를 찾을 수 없습니다.")
            continue
        
        issue_num = mapping[task_key]
        start_date = task_info['start_date']
        end_date = task_info['end_date']
        lane = normalize_lane_name(task_info['lane'])
        status = determine_status(start_date, end_date, current_date)
        
        # Issue 파일 찾기 및 업데이트
        issue_file = find_issue_file(task_key)
        if issue_file:
            update_issue_file(issue_file, start_date, end_date, lane)
            issues_updated.append({
                'task_key': task_key,
                'issue_num': issue_num,
                'file': issue_file.name,
                'start_date': start_date,
                'end_date': end_date,
                'lane': lane,
                'status': status
            })
        
        # gh CLI 명령어 생성 (실제 실행은 나중에)
        commands = []
        
        # Project 추가
        commands.append(['gh', 'issue', 'edit', str(issue_num), '--add-project', 'reacademix-backend'])
        
        # Date fields 추가 (GitHub Projects의 Date 필드)
        # Note: GitHub CLI의 date field 설정은 직접 지원하지 않으므로
        # Projects API를 사용하거나 수동으로 설정해야 할 수 있습니다.
        # 여기서는 명령어만 준비합니다.
        
        commands_executed.extend(commands)
    
    return issues_updated, commands_executed

def main():
    print("🚀 Gantt 차트 정보를 GitHub Issues에 동기화 시작...\n")
    
    # 1. Gantt 차트에서 Task 정보 파싱
    print("📊 Gantt 차트 파싱 중...")
    tasks = parse_gantt_table()
    print(f"✅ {len(tasks)}개의 Task 정보를 파싱했습니다.\n")
    
    # 2. Issue Index에서 매핑 정보 파싱
    print("🔗 Issue 매핑 정보 파싱 중...")
    mapping = parse_issue_index()
    print(f"✅ {len(mapping)}개의 Issue 매핑을 찾았습니다.\n")
    
    # 3. 현재 날짜 설정
    current_date = datetime.now().strftime('%Y-%m-%d')
    print(f"📅 현재 날짜: {current_date}\n")
    
    # 4. Issue 파일 업데이트
    print("📝 Issue 파일 업데이트 중...")
    issues_updated = []
    commands_to_execute = []
    
    for task_key, task_info in sorted(tasks.items()):
        if task_key not in mapping:
            print(f"⚠️  {task_key}: Issue #를 찾을 수 없습니다.")
            continue
        
        issue_num = mapping[task_key]
        start_date = task_info['start_date']
        end_date = task_info['end_date']
        lane = normalize_lane_name(task_info['lane'])
        status = determine_status(start_date, end_date, current_date)
        
        # Issue 파일 찾기 및 업데이트
        issue_file = find_issue_file(task_key)
        if issue_file:
            update_issue_file(issue_file, start_date, end_date, lane)
            issues_updated.append({
                'task_key': task_key,
                'issue_num': issue_num,
                'file': issue_file.name,
                'start_date': start_date,
                'end_date': end_date,
                'lane': lane,
                'status': status
            })
            print(f"✅ {task_key} (#{issue_num}): {issue_file.name} 업데이트 완료")
        else:
            print(f"⚠️  {task_key}: Issue 파일을 찾을 수 없습니다.")
        
        # gh CLI 명령어 준비
        commands_to_execute.append({
            'issue_num': issue_num,
            'task_key': task_key,
            'start_date': start_date,
            'end_date': end_date,
            'lane': lane,
            'status': status
        })
    
    print(f"\n✅ {len(issues_updated)}개의 Issue 파일을 업데이트했습니다.\n")
    
    # 5. gh CLI 명령어 실행
    print("🔧 GitHub Issues에 정보 반영 중...")
    print("⚠️  참고: GitHub Projects의 Date 필드는 API를 통해 설정해야 할 수 있습니다.\n")
    
    executed_commands = []
    failed_commands = []
    
    for cmd_info in commands_to_execute:
        issue_num = cmd_info['issue_num']
        task_key = cmd_info['task_key']
        
        # Project 추가
        success, output = run_gh_command(
            ['gh', 'issue', 'edit', str(issue_num), '--add-project', 'reacademix-backend'],
            f"Issue #{issue_num}에 Project 추가"
        )
        
        if success:
            executed_commands.append({
                'task_key': task_key,
                'issue_num': issue_num,
                'command': f"gh issue edit {issue_num} --add-project reacademix-backend",
                'result': 'success'
            })
        else:
            failed_commands.append({
                'task_key': task_key,
                'issue_num': issue_num,
                'command': f"gh issue edit {issue_num} --add-project reacademix-backend",
                'error': output
            })
        
        print(f"  {'✅' if success else '❌'} Issue #{issue_num} ({task_key}): Project 추가")
    
    # 6. 결과 요약 출력
    print("\n" + "="*80)
    print("📋 동기화 결과 요약")
    print("="*80)
    
    print(f"\n✅ 업데이트된 Issue 파일: {len(issues_updated)}개")
    print(f"✅ 성공한 gh 명령어: {len(executed_commands)}개")
    if failed_commands:
        print(f"❌ 실패한 gh 명령어: {len(failed_commands)}개")
    
    print("\n📝 업데이트된 Issue 목록:")
    for issue in issues_updated:
        print(f"  - {issue['task_key']} (Issue #{issue['issue_num']}): {issue['file']}")
        print(f"    Timeline: {issue['start_date']} ~ {issue['end_date']} | Lane: {issue['lane']} | Status: {issue['status']}")
    
    print("\n🔧 실행된 gh 명령어 목록:")
    for cmd in executed_commands:
        print(f"  ✅ {cmd['command']}")
    
    if failed_commands:
        print("\n❌ 실패한 명령어:")
        for cmd in failed_commands:
            print(f"  ❌ {cmd['command']}")
            print(f"     Error: {cmd['error'][:100]}")
    
    print("\n" + "="*80)
    print("⚠️  참고사항:")
    print("  - GitHub Projects의 Date 필드(Start Date, Due Date)는 GitHub CLI로 직접 설정할 수 없습니다.")
    print("  - Date 필드는 GitHub Projects 웹 UI에서 수동으로 설정하거나 Projects API를 사용해야 합니다.")
    print("  - Issue 본문에는 Timeline 정보가 추가되었으므로, 이를 참고하여 수동으로 설정할 수 있습니다.")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()

