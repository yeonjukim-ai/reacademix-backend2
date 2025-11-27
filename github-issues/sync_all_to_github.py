#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 Issue 파일을 업데이트하고 GitHub에 자동으로 반영하는 스크립트
"""

import re
import subprocess
from pathlib import Path

# Gantt 데이터와 Issue 번호 매핑
ISSUE_DATA = {
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

def update_issue_file(file_path, start_date, end_date, lane):
    """Issue 파일에 Timeline 섹션 추가/업데이트"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def update_github_issue(issue_num, file_path):
    """GitHub Issue 본문 업데이트 및 Project 추가"""
    results = []
    
    # 1. Issue 본문 업데이트
    try:
        result = subprocess.run(
            ['gh', 'issue', 'edit', str(issue_num), '--body-file', str(file_path)],
            capture_output=True,
            text=True,
            check=True
        )
        results.append(('body', True, f"Issue #{issue_num} 본문 업데이트 성공"))
    except subprocess.CalledProcessError as e:
        results.append(('body', False, f"Issue #{issue_num} 본문 업데이트 실패: {e.stderr[:100]}"))
    
    # 2. Project 추가
    try:
        result = subprocess.run(
            ['gh', 'issue', 'edit', str(issue_num), '--add-project', 'reacademix-backend'],
            capture_output=True,
            text=True,
            check=True
        )
        results.append(('project', True, f"Issue #{issue_num} Project 추가 성공"))
    except subprocess.CalledProcessError as e:
        results.append(('project', False, f"Issue #{issue_num} Project 추가 실패: {e.stderr[:100]}"))
    
    return results

def main():
    script_dir = Path(__file__).parent
    updated_files = []
    github_success = []
    github_failed = []
    
    print("=" * 80)
    print("GitHub Issues 및 Projects 자동 동기화")
    print("=" * 80)
    print()
    
    # Step 1: 모든 Issue 파일 업데이트
    print("Step 1: Issue 파일 업데이트 중...")
    for task_key, info in sorted(ISSUE_DATA.items()):
        files = list(script_dir.glob(f"{task_key}-*.md"))
        if files:
            file_path = files[0]
            update_issue_file(file_path, info['start'], info['end'], info['lane'])
            updated_files.append((task_key, file_path.name, info))
            print(f"  ✅ {task_key}: {file_path.name}")
        else:
            print(f"  ⚠️  {task_key}: 파일을 찾을 수 없습니다")
    
    print(f"\n✅ {len(updated_files)}개 파일 업데이트 완료\n")
    
    # Step 2: GitHub에 반영
    print("Step 2: GitHub Issues 및 Projects에 반영 중...")
    print()
    
    for task_key, file_name, info in updated_files:
        issue_num = info['issue']
        file_path = script_dir / file_name
        
        print(f"[{task_key}] Issue #{issue_num} 처리 중...")
        results = update_github_issue(issue_num, file_path)
        
        for result_type, success, message in results:
            if success:
                github_success.append((task_key, issue_num, result_type))
                print(f"  ✅ {message}")
            else:
                github_failed.append((task_key, issue_num, result_type, message))
                print(f"  ❌ {message}")
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("동기화 결과 요약")
    print("=" * 80)
    print(f"\n✅ 성공: {len(github_success)}개 작업")
    if github_failed:
        print(f"❌ 실패: {len(github_failed)}개 작업\n")
        print("실패한 작업:")
        for task_key, issue_num, result_type, message in github_failed:
            print(f"  - {task_key} (Issue #{issue_num}): {message}")
    else:
        print("❌ 실패: 없음")
    
    print("\n" + "=" * 80)
    print("완료!")
    print("=" * 80)
    print("\n참고:")
    print("- GitHub Projects의 Date 필드는 웹 UI에서 수동으로 설정하거나")
    print("  GitHub Projects API를 사용해야 합니다.")
    print("- Issue 본문의 Timeline 섹션을 참고하여 Date 필드를 설정하세요.")

if __name__ == '__main__':
    main()

