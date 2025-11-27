#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 Issue 파일 업데이트 및 GitHub 동기화 자동화
"""

import re
import subprocess
import sys
from pathlib import Path

TASKS = {
    'BE-INFRA-001': {'issue': 16, 'start': '2025-11-27', 'end': '2025-11-29', 'lane': 'Prerequisites'},
    'BE-INFRA-002': {'issue': 17, 'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Prerequisites'},
    'BE-INFRA-003': {'issue': 18, 'start': '2025-12-04', 'end': '2025-12-07', 'lane': 'Prerequisites'},
    'BE-COMMON-001': {'issue': 4, 'start': '2025-11-30', 'end': '2025-12-02', 'lane': 'Prerequisites'},
    'BE-COMMON-002': {'issue': 5, 'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Prerequisites'},
    'BE-COMMON-003': {'issue': 6, 'start': '2025-11-30', 'end': '2025-12-02', 'lane': 'Prerequisites'},
    'BE-AUTH-001': {'issue': 1, 'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Backend Core'},
    'BE-AUTH-002': {'issue': 2, 'start': '2025-12-12', 'end': '2025-12-14', 'lane': 'Backend Core'},
    'BE-AUTH-003': {'issue': 3, 'start': '2025-12-15', 'end': '2025-12-16', 'lane': 'Backend Core'},
    'BE-STUDENT-001': {'issue': 38, 'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-STUDENT-002': {'issue': 39, 'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-INTEGRATION-001': {'issue': 20, 'start': '2025-11-30', 'end': '2025-12-04', 'lane': 'Backend Core'},
    'BE-INTEGRATION-002': {'issue': 21, 'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Backend Core'},
    'BE-INTEGRATION-003': {'issue': 22, 'start': '2025-12-15', 'end': '2025-12-18', 'lane': 'Backend Core'},
    'BE-INTEGRATION-004': {'issue': 23, 'start': '2025-12-08', 'end': '2025-12-12', 'lane': 'Backend Core'},
    'BE-INTEGRATION-005': {'issue': 24, 'start': '2025-12-13', 'end': '2025-12-15', 'lane': 'Backend Core'},
    'BE-INTEGRATION-006': {'issue': 25, 'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Backend Core'},
    'BE-INTEGRATION-007': {'issue': 26, 'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-REPORT-001': {'issue': 30, 'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Backend Core'},
    'BE-REPORT-002': {'issue': 31, 'start': '2025-12-04', 'end': '2025-12-08', 'lane': 'Backend Core'},
    'BE-REPORT-003': {'issue': 32, 'start': '2025-12-19', 'end': '2025-12-24', 'lane': 'Backend Core'},
    'BE-REPORT-004': {'issue': 33, 'start': '2025-12-25', 'end': '2025-12-27', 'lane': 'Backend Core'},
    'BE-REPORT-005': {'issue': 34, 'start': '2025-12-25', 'end': '2025-12-26', 'lane': 'Backend Core'},
    'BE-REPORT-006': {'issue': 35, 'start': '2025-12-25', 'end': '2025-12-27', 'lane': 'Backend Core'},
    'BE-REPORT-007': {'issue': 36, 'start': '2025-12-27', 'end': '2025-12-29', 'lane': 'Backend Core'},
    'BE-EMAIL-001': {'issue': 14, 'start': '2025-12-09', 'end': '2025-12-12', 'lane': 'Backend Core'},
    'BE-EMAIL-002': {'issue': 15, 'start': '2025-12-25', 'end': '2025-12-28', 'lane': 'Backend Core'},
    'BE-DELIVERY-001': {'issue': 12, 'start': '2025-12-08', 'end': '2025-12-09', 'lane': 'Backend Core'},
    'BE-DELIVERY-002': {'issue': 13, 'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-INSIGHT-001': {'issue': 19, 'start': '2025-12-12', 'end': '2025-12-16', 'lane': 'AI Engine'},
    'BE-DATA-001': {'issue': 7, 'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-002': {'issue': 8, 'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-003': {'issue': 9, 'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-004': {'issue': 10, 'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-005': {'issue': 11, 'start': '2025-12-08', 'end': '2025-12-10', 'lane': 'Financial'},
    'BE-SECURITY-001': {'issue': 37, 'start': '2025-12-08', 'end': '2025-12-12', 'lane': 'NFR'},
    'BE-PERF-001': {'issue': 27, 'start': '2025-12-25', 'end': '2025-12-29', 'lane': 'NFR'},
    'BE-PERF-002': {'issue': 28, 'start': '2025-12-25', 'end': '2025-12-29', 'lane': 'NFR'},
    'BE-PERF-003': {'issue': 29, 'start': '2025-12-04', 'end': '2025-12-08', 'lane': 'NFR'},
}

def update_file(file_path, start, end, lane):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    timeline = f"\n## ⏱ 일정(Timeline)\n\n- **Start**: {start}\n- **End**: {end}\n- **Lane**: {lane}\n"
    
    if '## ⏱ 일정(Timeline)' in content:
        pattern = r'## ⏱[️]? 일정\(Timeline\).*?(?=\n## |\Z)'
        content = re.sub(pattern, timeline.strip(), content, flags=re.DOTALL)
    elif '## 🔗 Traceability' in content:
        content = content.replace('## 🔗 Traceability', timeline + '\n## 🔗 Traceability')
    else:
        content += timeline
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def run_gh(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    script_dir = Path(__file__).parent
    
    print("="*80)
    print("GitHub Issues 및 Projects 자동 동기화")
    print("="*80)
    print()
    
    # Step 1: 파일 업데이트
    print("Step 1: Issue 파일 업데이트...")
    updated = []
    for key, info in sorted(TASKS.items()):
        files = list(script_dir.glob(f"{key}-*.md"))
        if files:
            update_file(files[0], info['start'], info['end'], info['lane'])
            updated.append((key, files[0], info))
    
    print(f"✅ {len(updated)}개 파일 업데이트 완료\n")
    
    # Step 2: GitHub 동기화
    print("Step 2: GitHub Issues 및 Projects 동기화...")
    print()
    
    commands = []
    for key, file_path, info in updated:
        issue_num = info['issue']
        commands.append(f'gh issue edit {issue_num} --body-file "{file_path.name}"')
        commands.append(f'gh issue edit {issue_num} --add-project reacademix-backend')
    
    # 명령어를 파일로 저장
    commands_file = script_dir / 'execute_github_sync.sh'
    with open(commands_file, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        f.write("# GitHub Issues 및 Projects 동기화 명령어\n\n")
        for cmd in commands:
            f.write(cmd + "\n")
    
    print(f"✅ 명령어 파일 생성: {commands_file.name}")
    print(f"   총 {len(commands)}개 명령어 준비됨")
    print()
    print("실행 방법:")
    print(f"  bash {commands_file.name}")
    print()
    print("또는 PowerShell에서:")
    print(f"  Get-Content {commands_file.name} | ForEach-Object {{ Invoke-Expression $_ }}")
    print()
    print("="*80)

if __name__ == '__main__':
    main()

