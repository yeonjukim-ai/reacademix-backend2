#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 GitHub Issue 파일에 Timeline 섹션을 추가하는 스크립트
"""

import re
from pathlib import Path

# Gantt 테이블 데이터
GANTT_DATA = {
    'BE-INFRA-001': {'start': '2025-11-27', 'end': '2025-11-29', 'lane': 'Prerequisites'},
    'BE-INFRA-002': {'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Prerequisites'},
    'BE-INFRA-003': {'start': '2025-12-04', 'end': '2025-12-07', 'lane': 'Prerequisites'},
    'BE-COMMON-001': {'start': '2025-11-30', 'end': '2025-12-02', 'lane': 'Prerequisites'},
    'BE-COMMON-002': {'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Prerequisites'},
    'BE-COMMON-003': {'start': '2025-11-30', 'end': '2025-12-02', 'lane': 'Prerequisites'},
    'BE-AUTH-001': {'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Backend Core'},
    'BE-AUTH-002': {'start': '2025-12-12', 'end': '2025-12-14', 'lane': 'Backend Core'},
    'BE-AUTH-003': {'start': '2025-12-15', 'end': '2025-12-16', 'lane': 'Backend Core'},
    'BE-STUDENT-001': {'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-STUDENT-002': {'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-INTEGRATION-001': {'start': '2025-11-30', 'end': '2025-12-04', 'lane': 'Backend Core'},
    'BE-INTEGRATION-002': {'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Backend Core'},
    'BE-INTEGRATION-003': {'start': '2025-12-15', 'end': '2025-12-18', 'lane': 'Backend Core'},
    'BE-INTEGRATION-004': {'start': '2025-12-08', 'end': '2025-12-12', 'lane': 'Backend Core'},
    'BE-INTEGRATION-005': {'start': '2025-12-13', 'end': '2025-12-15', 'lane': 'Backend Core'},
    'BE-INTEGRATION-006': {'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Backend Core'},
    'BE-INTEGRATION-007': {'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-REPORT-001': {'start': '2025-11-30', 'end': '2025-12-03', 'lane': 'Backend Core'},
    'BE-REPORT-002': {'start': '2025-12-04', 'end': '2025-12-08', 'lane': 'Backend Core'},
    'BE-REPORT-003': {'start': '2025-12-19', 'end': '2025-12-24', 'lane': 'Backend Core'},
    'BE-REPORT-004': {'start': '2025-12-25', 'end': '2025-12-27', 'lane': 'Backend Core'},
    'BE-REPORT-005': {'start': '2025-12-25', 'end': '2025-12-26', 'lane': 'Backend Core'},
    'BE-REPORT-006': {'start': '2025-12-25', 'end': '2025-12-27', 'lane': 'Backend Core'},
    'BE-REPORT-007': {'start': '2025-12-27', 'end': '2025-12-29', 'lane': 'Backend Core'},
    'BE-EMAIL-001': {'start': '2025-12-09', 'end': '2025-12-12', 'lane': 'Backend Core'},
    'BE-EMAIL-002': {'start': '2025-12-25', 'end': '2025-12-28', 'lane': 'Backend Core'},
    'BE-DELIVERY-001': {'start': '2025-12-08', 'end': '2025-12-09', 'lane': 'Backend Core'},
    'BE-DELIVERY-002': {'start': '2025-12-15', 'end': '2025-12-17', 'lane': 'Backend Core'},
    'BE-INSIGHT-001': {'start': '2025-12-12', 'end': '2025-12-16', 'lane': 'AI Engine'},
    'BE-DATA-001': {'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-002': {'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-003': {'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-004': {'start': '2025-12-08', 'end': '2025-12-11', 'lane': 'Financial'},
    'BE-DATA-005': {'start': '2025-12-08', 'end': '2025-12-10', 'lane': 'Financial'},
    'BE-SECURITY-001': {'start': '2025-12-08', 'end': '2025-12-12', 'lane': 'NFR'},
    'BE-PERF-001': {'start': '2025-12-25', 'end': '2025-12-29', 'lane': 'NFR'},
    'BE-PERF-002': {'start': '2025-12-25', 'end': '2025-12-29', 'lane': 'NFR'},
    'BE-PERF-003': {'start': '2025-12-04', 'end': '2025-12-08', 'lane': 'NFR'},
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

def main():
    script_dir = Path(__file__).parent
    updated = []
    not_found = []
    
    print("=" * 80)
    print("GitHub Issue 파일에 Timeline 섹션 추가")
    print("=" * 80)
    print()
    
    for task_key, info in sorted(GANTT_DATA.items()):
        # 파일 찾기
        files = list(script_dir.glob(f"{task_key}-*.md"))
        if files:
            file_path = files[0]
            update_issue_file(file_path, info['start'], info['end'], info['lane'])
            updated.append((task_key, file_path.name, info))
            print(f"✅ {task_key}: {file_path.name}")
        else:
            not_found.append(task_key)
            print(f"⚠️  {task_key}: 파일을 찾을 수 없습니다")
    
    print()
    print("=" * 80)
    print(f"✅ {len(updated)}개 파일 업데이트 완료")
    if not_found:
        print(f"⚠️  {len(not_found)}개 파일을 찾을 수 없습니다: {', '.join(not_found)}")
    print("=" * 80)

if __name__ == '__main__':
    main()

