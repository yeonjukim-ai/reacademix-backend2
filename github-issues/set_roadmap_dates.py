#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Projects v2 Roadmap에 날짜 필드를 설정하는 스크립트
Execution Plan 문서의 일정을 기반으로 각 이슈에 Start Date와 End Date를 설정합니다.
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Task ID → Issue 번호 매핑
ISSUE_MAPPING = {
    'BE-AUTH-001': 1, 'BE-AUTH-002': 2, 'BE-AUTH-003': 3,
    'BE-COMMON-001': 4, 'BE-COMMON-002': 5, 'BE-COMMON-003': 6,
    'BE-DATA-001': 7, 'BE-DATA-002': 8, 'BE-DATA-003': 9,
    'BE-DATA-004': 10, 'BE-DATA-005': 11,
    'BE-DELIVERY-001': 12, 'BE-DELIVERY-002': 13,
    'BE-EMAIL-001': 14, 'BE-EMAIL-002': 15,
    'BE-INFRA-001': 16, 'BE-INFRA-002': 17, 'BE-INFRA-003': 18,
    'BE-INSIGHT-001': 19,
    'BE-INTEGRATION-001': 20, 'BE-INTEGRATION-002': 21,
    'BE-INTEGRATION-003': 22, 'BE-INTEGRATION-004': 23,
    'BE-INTEGRATION-005': 24, 'BE-INTEGRATION-006': 25,
    'BE-INTEGRATION-007': 26,
    'BE-PERF-001': 27, 'BE-PERF-002': 28, 'BE-PERF-003': 29,
    'BE-REPORT-001': 30, 'BE-REPORT-002': 31, 'BE-REPORT-003': 32,
    'BE-REPORT-004': 33, 'BE-REPORT-005': 34, 'BE-REPORT-006': 35,
    'BE-REPORT-007': 36,
    'BE-SECURITY-001': 37,
    'BE-STUDENT-001': 38, 'BE-STUDENT-002': 39,
}

# Execution Plan 기반 일정 (Day 기준, 시작일: 2025-01-27)
# Phase 1: Day 1-15 (Week 1-2)
# Phase 2: Day 16-30 (Week 3-5)
# Phase 3: Day 23-42 (Week 6-9)
# Phase 4: Day 43-55 (Week 10-11)

BASE_DATE = datetime(2025, 1, 27)  # 프로젝트 시작일

# 각 이슈의 일정 (Day 범위)
ISSUE_SCHEDULE = {
    # Wave 1: 인프라 설정
    'BE-INFRA-001': (1, 3),      # Day 1-3
    'BE-INFRA-002': (4, 6),      # Day 4-6
    'BE-INFRA-003': (7, 9),      # Day 7-9
    'BE-COMMON-001': (2, 3),     # Day 2-3
    'BE-COMMON-002': (2, 3),     # Day 2-3
    'BE-COMMON-003': (2, 3),     # Day 2-3
    
    # Wave 2: 인증
    'BE-AUTH-001': (10, 12),     # Day 10-12
    'BE-AUTH-002': (13, 14),     # Day 13-14
    'BE-AUTH-003': (15, 15),     # Day 15
    
    # Wave 3: 학생 관리
    'BE-STUDENT-001': (16, 17), # Day 16-17
    'BE-STUDENT-002': (16, 17), # Day 16-17
    
    # Wave 4: 데이터 통합
    'BE-INTEGRATION-001': (11, 13),  # Day 11-13
    'BE-INTEGRATION-002': (11, 13),  # Day 11-13
    'BE-INTEGRATION-003': (18, 20),  # Day 18-20
    'BE-INTEGRATION-004': (18, 20),  # Day 18-20
    'BE-INTEGRATION-005': (21, 22),  # Day 21-22
    'BE-INTEGRATION-006': (18, 20),  # Day 18-20
    'BE-INTEGRATION-007': (21, 22),  # Day 21-22
    
    # Wave 5: 리포트 생성
    'BE-DATA-001': (23, 24),     # Day 23-24
    'BE-DATA-002': (23, 24),     # Day 23-24
    'BE-DATA-003': (23, 24),     # Day 23-24
    'BE-DATA-004': (23, 24),     # Day 23-24
    'BE-DATA-005': (25, 25),     # Day 25
    'BE-INSIGHT-001': (26, 28),  # Day 26-28
    'BE-REPORT-001': (11, 12),   # Day 11-12
    'BE-REPORT-002': (13, 15),   # Day 13-15
    'BE-REPORT-003': (29, 33),   # Day 29-33
    'BE-REPORT-004': (34, 35),   # Day 34-35
    'BE-REPORT-005': (34, 34),   # Day 34
    'BE-REPORT-006': (36, 37),   # Day 36-37
    'BE-REPORT-007': (36, 37),   # Day 36-37
    
    # Wave 6: 리포트 전송
    'BE-EMAIL-001': (38, 39),    # Day 38-39
    'BE-EMAIL-002': (40, 42),    # Day 40-42
    'BE-DELIVERY-001': (34, 34), # Day 34
    'BE-DELIVERY-002': (40, 41), # Day 40-41
    
    # Wave 7: 비기능
    'BE-SECURITY-001': (38, 40), # Day 38-40
    'BE-PERF-001': (43, 45),    # Day 43-45
    'BE-PERF-002': (43, 45),    # Day 43-45
    'BE-PERF-003': (43, 45),    # Day 43-45
}

PROJECT_NUMBER = 5
REPO_OWNER = "yeonjukim-ai"
REPO_NAME = "reacademix-backend2"

def get_project_id():
    """프로젝트 ID 가져오기"""
    query = f'''
    query {{
      viewer {{
        projectV2(number: {PROJECT_NUMBER}) {{
          id
          title
        }}
      }}
    }}
    '''
    
    try:
        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            project = data.get('data', {}).get('viewer', {}).get('projectV2')
            if project:
                return project.get('id'), project.get('title')
        return None, None
    except Exception as e:
        print(f"프로젝트 조회 오류: {e}")
        return None, None

def get_project_fields(project_id):
    """프로젝트의 필드 목록 가져오기 (Date 필드 찾기)"""
    query = '''
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 20) {
            nodes {
              ... on ProjectV2Field {
                id
                name
                dataType
              }
              ... on ProjectV2IterationField {
                id
                name
                dataType
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                dataType
              }
            }
          }
        }
      }
    }
    '''
    
    try:
        variables = json.dumps({"projectId": project_id})
        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}', '-f', f'variables={variables}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            errors = data.get('errors', [])
            if errors:
                print(f"  GraphQL 오류: {json.dumps(errors, indent=2)}")
            
            node = data.get('data', {}).get('node', {})
            if not node:
                print(f"  응답 데이터: {json.dumps(data, indent=2)}")
                return None, None, []
            
            fields = node.get('fields', {}).get('nodes', [])
            
            print(f"  조회된 필드 수: {len(fields)}")
            for field in fields:
                print(f"    - {field.get('name')} ({field.get('dataType')})")
            
            start_date_field = None
            end_date_field = None
            
            for field in fields:
                name = field.get('name', '')
                data_type = field.get('dataType', '')
                field_id = field.get('id')
                
                # Date 타입 필드 찾기
                if data_type == 'DATE':
                    name_lower = name.lower()
                    if 'start' in name_lower:
                        start_date_field = field_id
                        print(f"  ✅ Start Date 필드 발견: {name} ({field_id[:20]}...)")
                    elif 'end' in name_lower:
                        end_date_field = field_id
                        print(f"  ✅ End Date 필드 발견: {name} ({field_id[:20]}...)")
                    elif not start_date_field:
                        # Date 필드가 하나만 있는 경우
                        start_date_field = field_id
                        end_date_field = field_id
                        print(f"  ✅ Date 필드 발견: {name} ({field_id[:20]}...)")
            
            return start_date_field, end_date_field, fields
        else:
            print(f"  명령어 실행 실패: {result.stderr}")
            print(f"  응답: {result.stdout}")
        return None, None, []
    except Exception as e:
        print(f"필드 조회 오류: {e}")
        return None, None, []

def get_issue_node_id(issue_number):
    """이슈 노드 ID 가져오기"""
    query = f'''
    query {{
      repository(owner: "{REPO_OWNER}", name: "{REPO_NAME}") {{
        issue(number: {issue_number}) {{
          id
          title
        }}
      }}
    }}
    '''
    
    try:
        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            issue = data.get('data', {}).get('repository', {}).get('issue')
            if issue:
                return issue.get('id'), issue.get('title')
        return None, None
    except Exception as e:
        return None, None

def get_project_item_id(project_id, issue_id):
    """프로젝트 아이템 ID 가져오기"""
    query = f'''
    query {{
      node(id: "{project_id}") {{
        ... on ProjectV2 {{
          items(first: 100) {{
            nodes {{
              id
              content {{
                ... on Issue {{
                  id
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    
    try:
        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={query}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            node = data.get('data', {}).get('node', {})
            items = node.get('items', {}).get('nodes', [])
            
            for item in items:
                content = item.get('content', {})
                if content.get('id') == issue_id:
                    return item.get('id')
        return None
    except Exception as e:
        return None

def update_project_item_date(project_id, item_id, field_id, date_value):
    """프로젝트 아이템의 날짜 필드 업데이트"""
    mutation = f'''
    mutation {{
      updateProjectV2ItemFieldValue(input: {{
        projectId: "{project_id}"
        itemId: "{item_id}"
        fieldId: "{field_id}"
        value: {{
          date: "{date_value}"
        }}
      }}) {{
        projectV2Item {{
          id
        }}
      }}
    }}
    '''
    
    try:
        result = subprocess.run(
            ['gh', 'api', 'graphql', '-f', f'query={mutation}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            errors = data.get('errors', [])
            if errors:
                return False, errors[0].get('message', 'Unknown error')
            return True, "success"
        return False, result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("GitHub Projects Roadmap 날짜 설정")
    print("=" * 80)
    print(f"프로젝트 번호: {PROJECT_NUMBER}")
    print(f"저장소: {REPO_OWNER}/{REPO_NAME}")
    print(f"기준일: {BASE_DATE.strftime('%Y-%m-%d')}")
    print()
    
    # 프로젝트 ID 가져오기
    print("프로젝트 정보 조회 중...")
    project_id, project_title = get_project_id()
    
    if not project_id:
        print("❌ 프로젝트를 찾을 수 없습니다.")
        return
    
    print(f"✅ 프로젝트 찾음: {project_title}")
    print()
    
    # 프로젝트 필드 가져오기
    print("프로젝트 필드 조회 중...")
    start_field_id, end_field_id, all_fields = get_project_fields(project_id)
    
    if not start_field_id:
        print("❌ Date 필드를 찾을 수 없습니다.")
        print("\n사용 가능한 필드:")
        for field in all_fields:
            print(f"  - {field.get('name')} ({field.get('dataType')})")
        print("\n⚠️  GitHub Projects에서 Date 필드를 생성해야 합니다.")
        print("   필드 이름: 'Start date' 또는 'Date'")
        return
    
    print(f"✅ Start Date 필드: {start_field_id[:20]}...")
    if end_field_id and end_field_id != start_field_id:
        print(f"✅ End Date 필드: {end_field_id[:20]}...")
    else:
        print("⚠️  End Date 필드가 없습니다. Start Date만 사용합니다.")
        end_field_id = start_field_id
    print()
    
    # 사용자 확인
    response = input(f"총 {len(ISSUE_MAPPING)}개의 이슈에 날짜를 설정하시겠습니까? (y/n): ")
    if response.lower() != 'y':
        print("취소되었습니다.")
        return
    
    print()
    print("날짜 설정 시작...")
    print()
    
    success_count = 0
    fail_count = 0
    
    for task_id, issue_number in sorted(ISSUE_MAPPING.items(), key=lambda x: x[1]):
        if task_id not in ISSUE_SCHEDULE:
            print(f"[{task_id}] Issue #{issue_number}: 일정 정보 없음, 건너뜀")
            continue
        
        start_day, end_day = ISSUE_SCHEDULE[task_id]
        start_date = BASE_DATE + timedelta(days=start_day - 1)
        end_date = BASE_DATE + timedelta(days=end_day - 1)
        
        print(f"[{task_id}] Issue #{issue_number} ({start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')})...", end=" ")
        
        # 이슈 노드 ID 가져오기
        issue_id, issue_title = get_issue_node_id(issue_number)
        if not issue_id:
            print("❌ 이슈를 찾을 수 없습니다")
            fail_count += 1
            continue
        
        # 프로젝트 아이템 ID 가져오기
        item_id = get_project_item_id(project_id, issue_id)
        if not item_id:
            print("❌ 프로젝트 아이템을 찾을 수 없습니다 (프로젝트에 추가되지 않음)")
            fail_count += 1
            continue
        
        # Start Date 설정
        success, message = update_project_item_date(
            project_id, item_id, start_field_id, start_date.strftime('%Y-%m-%d')
        )
        
        if not success:
            print(f"❌ Start Date 설정 실패: {message}")
            fail_count += 1
            continue
        
        # End Date 설정 (Start Date와 다른 경우)
        if end_field_id != start_field_id or end_date != start_date:
            success, message = update_project_item_date(
                project_id, item_id, end_field_id, end_date.strftime('%Y-%m-%d')
            )
            if not success:
                print(f"⚠️  End Date 설정 실패: {message} (Start Date는 설정됨)")
        
        print("✅ 성공")
        success_count += 1
    
    # 결과 요약
    print()
    print("=" * 80)
    print("결과 요약")
    print("=" * 80)
    print(f"✅ 성공: {success_count}개")
    if fail_count > 0:
        print(f"❌ 실패: {fail_count}개")
    print("=" * 80)
    
    if success_count > 0:
        print()
        print("✅ 작업 완료!")
        print(f"Roadmap에서 확인: https://github.com/users/{REPO_OWNER}/projects/{PROJECT_NUMBER}")

if __name__ == '__main__':
    main()

