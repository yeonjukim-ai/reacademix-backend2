#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 Issue 파일 업데이트 및 GitHub 동기화 완전 자동화 스크립트
"""

import re
import subprocess
import sys
from pathlib import Path

# 모든 Task 정보
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
    """Issue 파일에 Timeline 섹션 추가"""
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

def main():
    script_dir = Path(__file__).parent
    updated = []
    
    print("="*80)
    print("Issue 파일 업데이트 및 GitHub 동기화")
    print("="*80)
    print()
    
    # 파일 업데이트
    print("Step 1: Issue 파일 업데이트...")
    for key, info in sorted(TASKS.items()):
        files = list(script_dir.glob(f"{key}-*.md"))
        if files:
            update_file(files[0], info['start'], info['end'], info['lane'])
            updated.append((key, files[0], info))
            print(f"  ✓ {key}")
    
    print(f"\n{len(updated)}개 파일 업데이트 완료\n")
    
    # GitHub 동기화
    print("Step 2: GitHub Issues 및 Projects 동기화...")
    print()
    
    success_body = 0
    success_project = 0
    failed = []
    
    for key, file_path, info in updated:
        issue_num = info['issue']
        print(f"[{key}] Issue #{issue_num}...", end=" ")
        
        # 본문 업데이트
        try:
            subprocess.run(['gh', 'issue', 'edit', str(issue_num), '--body-file', str(file_path)],
                          capture_output=True, check=True)
            success_body += 1
            print("본문✓", end=" ")
        except:
            failed.append(f"{key} 본문")
            print("본문✗", end=" ")
        
        # Project 추가
        try:
            subprocess.run(['gh', 'issue', 'edit', str(issue_num), '--add-project', 'reacademix-backend'],
                          capture_output=True, check=True)
            success_project += 1
            print("Project✓")
        except:
            failed.append(f"{key} Project")
            print("Project✗")
    
    print("\n" + "="*80)
    print("결과:")
    print(f"  본문 업데이트: {success_body}/{len(updated)} 성공")
    print(f"  Project 추가: {success_project}/{len(updated)} 성공")
    if failed:
        print(f"  실패: {len(failed)}개")
    print("="*80)

if __name__ == '__main__':
    main()

