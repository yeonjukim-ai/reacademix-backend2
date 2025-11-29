#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Projects v2 API를 사용하여 이슈를 프로젝트에 추가하는 스크립트
프로젝트 번호: 5 (reacademix-backend2)
저장소: yeonjukim-ai/reacademix-backend2
"""

import subprocess
import json
import sys
from pathlib import Path

# Task ID → Issue 번호 매핑 (새로 생성된 이슈 번호)
ISSUE_MAPPING = {
    'BE-AUTH-001': 1,
    'BE-AUTH-002': 2,
    'BE-AUTH-003': 3,
    'BE-COMMON-001': 4,
    'BE-COMMON-002': 5,
    'BE-COMMON-003': 6,
    'BE-DATA-001': 7,
    'BE-DATA-002': 8,
    'BE-DATA-003': 9,
    'BE-DATA-004': 10,
    'BE-DATA-005': 11,
    'BE-DELIVERY-001': 12,
    'BE-DELIVERY-002': 13,
    'BE-EMAIL-001': 14,
    'BE-EMAIL-002': 15,
    'BE-INFRA-001': 16,
    'BE-INFRA-002': 17,
    'BE-INFRA-003': 18,
    'BE-INSIGHT-001': 19,
    'BE-INTEGRATION-001': 20,
    'BE-INTEGRATION-002': 21,
    'BE-INTEGRATION-003': 22,
    'BE-INTEGRATION-004': 23,
    'BE-INTEGRATION-005': 24,
    'BE-INTEGRATION-006': 25,
    'BE-INTEGRATION-007': 26,
    'BE-PERF-001': 27,
    'BE-PERF-002': 28,
    'BE-PERF-003': 29,
    'BE-REPORT-001': 30,
    'BE-REPORT-002': 31,
    'BE-REPORT-003': 32,
    'BE-REPORT-004': 33,
    'BE-REPORT-005': 34,
    'BE-REPORT-006': 35,
    'BE-REPORT-007': 36,
    'BE-SECURITY-001': 37,
    'BE-STUDENT-001': 38,
    'BE-STUDENT-002': 39,
}

PROJECT_NUMBER = 5
REPO_OWNER = "yeonjukim-ai"
REPO_NAME = "reacademix-backend2"

def get_project_id():
    """프로젝트 번호로 프로젝트 ID 가져오기"""
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
            errors = data.get('errors', [])
            
            if errors:
                error_msg = errors[0].get('message', 'Unknown error')
                print(f"❌ GraphQL 오류: {error_msg}")
                if 'INSUFFICIENT_SCOPES' in error_msg or 'scopes' in error_msg.lower():
                    print("\n⚠️  권한이 필요합니다. 다음 명령어를 실행하세요:")
                    print("   gh auth refresh -s read:project,write:project")
                return None, None
            
            project = data.get('data', {}).get('viewer', {}).get('projectV2')
            
            if project:
                return project.get('id'), project.get('title')
            else:
                print(f"❌ 프로젝트를 찾을 수 없습니다. 응답: {json.dumps(data, indent=2)}")
                return None, None
        else:
            print(f"❌ 명령어 실행 실패: {result.stderr}")
            print(f"응답: {result.stdout}")
            return None, None
    except Exception as e:
        print(f"프로젝트 조회 오류: {e}")
        return None, None

def get_issue_node_id(issue_number):
    """이슈 번호로 이슈 노드 ID 가져오기"""
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
            errors = data.get('errors', [])
            
            if errors:
                error_msg = errors[0].get('message', 'Unknown error')
                print(f"  ❌ GraphQL 오류: {error_msg}")
                return None, None
            
            issue = data.get('data', {}).get('repository', {}).get('issue')
            
            if issue:
                return issue.get('id'), issue.get('title')
        
        return None, None
    except Exception as e:
        print(f"  ❌ 이슈 조회 오류: {e}")
        return None, None

def add_issue_to_project(project_id, issue_id):
    """프로젝트에 이슈 추가"""
    mutation = f'''
    mutation {{
      addProjectV2ItemById(input: {{
        projectId: "{project_id}"
        contentId: "{issue_id}"
      }}) {{
        item {{
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
                error_msg = errors[0].get('message', 'Unknown error')
                # 이미 추가된 경우도 성공으로 간주
                if 'already' in error_msg.lower() or 'duplicate' in error_msg.lower():
                    return True, "already_added"
                return False, error_msg
            
            item = data.get('data', {}).get('addProjectV2ItemById', {}).get('item')
            if item:
                return True, "success"
        
        return False, result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("GitHub Projects v2에 이슈 추가")
    print("=" * 80)
    print(f"프로젝트 번호: {PROJECT_NUMBER}")
    print(f"저장소: {REPO_OWNER}/{REPO_NAME}")
    print(f"프로젝트 URL: https://github.com/users/{REPO_OWNER}/projects/{PROJECT_NUMBER}")
    print()
    
    # 프로젝트 ID 가져오기
    print("프로젝트 정보 조회 중...")
    project_id, project_title = get_project_id()
    
    if not project_id:
        print("\n❌ 프로젝트를 찾을 수 없거나 권한이 없습니다.")
        print("\n해결 방법:")
        print("1. GitHub CLI 권한 갱신:")
        print("   gh auth refresh -s read:project,write:project")
        print("2. 또는 웹 UI에서 수동으로 추가:")
        print(f"   https://github.com/users/{REPO_OWNER}/projects/{PROJECT_NUMBER}")
        return
    
    print(f"✅ 프로젝트 찾음: {project_title} (ID: {project_id[:20]}...)")
    print()
    
    # 사용자 확인
    response = input(f"총 {len(ISSUE_MAPPING)}개의 이슈를 프로젝트에 추가하시겠습니까? (y/n): ")
    if response.lower() != 'y':
        print("취소되었습니다.")
        return
    
    print()
    print("이슈 추가 시작...")
    print()
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for task_id, issue_number in sorted(ISSUE_MAPPING.items(), key=lambda x: x[1]):
        print(f"[{task_id}] Issue #{issue_number} 처리 중...", end=" ")
        
        # 이슈 노드 ID 가져오기
        issue_id, issue_title = get_issue_node_id(issue_number)
        
        if not issue_id:
            print("❌ 이슈를 찾을 수 없습니다")
            fail_count += 1
            continue
        
        # 프로젝트에 추가
        success, message = add_issue_to_project(project_id, issue_id)
        
        if success:
            if message == "already_added":
                print("⏭️  이미 추가됨")
                skip_count += 1
            else:
                print("✅ 성공")
                success_count += 1
        else:
            print(f"❌ 실패: {message}")
            fail_count += 1
    
    # 결과 요약
    print()
    print("=" * 80)
    print("결과 요약")
    print("=" * 80)
    print(f"✅ 성공: {success_count}개")
    if skip_count > 0:
        print(f"⏭️  이미 추가됨: {skip_count}개")
    if fail_count > 0:
        print(f"❌ 실패: {fail_count}개")
    print("=" * 80)
    
    if success_count > 0 or skip_count > 0:
        print()
        print("✅ 작업 완료!")
        print(f"프로젝트 페이지에서 확인: https://github.com/users/{REPO_OWNER}/projects/{PROJECT_NUMBER}")
    elif fail_count > 0:
        print()
        print("⚠️  일부 이슈 추가에 실패했습니다.")
        print("권한을 갱신한 후 다시 시도하세요:")
        print("   gh auth refresh -s read:project,write:project")

if __name__ == '__main__':
    main()

