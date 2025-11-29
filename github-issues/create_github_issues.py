import os
import re
import subprocess
import json
from pathlib import Path

def parse_markdown_file(filepath):
    """마크다운 파일을 파싱하여 title과 body 추출"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 첫 번째 줄에서 제목 추출 (# 제목)
    lines = content.split('\n')
    title = lines[0].replace('# ', '').strip()
    
    # 나머지 전체를 body로 사용
    body = '\n'.join(lines[1:]).strip()
    
    # Type 추출 (라벨용)
    type_match = re.search(r'- \*\*Type\*\*: (.+)', content)
    issue_type = type_match.group(1).strip() if type_match else "Functional"
    
    # Key 추출
    key_match = re.search(r'- \*\*Key\*\*: (.+)', content)
    key = key_match.group(1).strip() if key_match else ""
    
    return title, body, issue_type, key

def get_labels(issue_type):
    """Type에 따라 라벨 리스트 반환"""
    base_labels = ["backend"]
    
    if issue_type == "Functional":
        return base_labels + ["feature"]
    elif issue_type == "Non-Functional":
        return base_labels + ["non-functional"]
    elif issue_type == "Infrastructure":
        return base_labels + ["infrastructure"]
    else:
        return base_labels

def create_github_issue(title, body, labels, key):
    """GitHub CLI를 사용하여 이슈 생성"""
    # body를 임시 파일로 저장 (긴 본문 처리)
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.md', delete=False) as f:
        f.write(body)
        body_file = f.name
    
    try:
        # GitHub CLI 명령 실행 (올바른 저장소 지정)
        cmd = [
            'gh', 'issue', 'create',
            '--repo', 'yeonjukim-ai/reacademix-backend2',
            '--title', title,
            '--body-file', body_file
        ]
        
        # 라벨이 있으면 추가 (라벨이 없어도 이슈는 생성되도록)
        if labels:
            # 각 라벨을 개별적으로 추가 시도
            for label in labels:
                cmd.extend(['--label', label])
        
        print(f"실행 명령: gh issue create --title \"{title[:50]}...\" --body-file <temp_file> --label {' '.join(labels) if labels else 'none'}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            # 생성된 이슈 URL에서 번호 추출
            output = result.stdout.strip()
            # URL 형식: https://github.com/owner/repo/issues/123
            issue_match = re.search(r'/issues/(\d+)', output)
            issue_number = issue_match.group(1) if issue_match else None
            return issue_number, output
        else:
            error_msg = result.stderr.strip()
            # 라벨 관련 에러인 경우 라벨 없이 재시도
            if 'label' in error_msg.lower() or 'Label' in error_msg:
                print(f"  ⚠️  라벨 에러 감지, 라벨 없이 재시도...")
                cmd_no_label = [
                    'gh', 'issue', 'create',
                    '--repo', 'yeonjukim-ai/reacademix-backend2',
                    '--title', title,
                    '--body-file', body_file
                ]
                result = subprocess.run(cmd_no_label, capture_output=True, text=True, encoding='utf-8')
                if result.returncode == 0:
                    output = result.stdout.strip()
                    issue_match = re.search(r'/issues/(\d+)', output)
                    issue_number = issue_match.group(1) if issue_match else None
                    return issue_number, output
            print(f"에러: {error_msg}")
            return None, None
    finally:
        # 임시 파일 삭제
        if os.path.exists(body_file):
            os.unlink(body_file)

def main():
    # 현재 디렉토리의 모든 .md 파일 찾기 (backend-tasks.json 제외)
    md_files = sorted([f for f in os.listdir('.') if f.endswith('.md') and f.startswith('BE-')])
    
    if not md_files:
        print("마크다운 파일을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(md_files)}개의 마크다운 파일을 찾았습니다.\n")
    
    # 예시 명령 보여주기 (처음 2개)
    print("=" * 80)
    print("예시 명령 (처음 2개 파일 기준):")
    print("=" * 80)
    
    for i, md_file in enumerate(md_files[:2]):
        filepath = Path(md_file)
        title, body, issue_type, key = parse_markdown_file(filepath)
        labels = get_labels(issue_type)
        labels_str = ','.join(labels)
        
        print(f"\n[{i+1}] {md_file}")
        print(f"  Key: {key}")
        print(f"  Type: {issue_type}")
        print(f"  Title: {title}")
        print(f"  Labels: {labels_str}")
        print(f"  명령:")
        print(f"    gh issue create --title \"{title}\" --body-file <temp_file> --label \"{labels_str}\"")
        print()
    
    print("=" * 80)
    print("\n⚠️  주의: GitHub CLI 인증이 필요합니다.")
    print("인증 상태 확인 중...\n")
    
    # 인증 상태 확인
    auth_check = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, encoding='utf-8')
    if auth_check.returncode != 0:
        print("❌ GitHub CLI 인증이 되어 있지 않습니다.")
        print("\n다음 명령으로 인증하세요:")
        print("  gh auth login")
        print("\n또는 GH_TOKEN 환경 변수를 설정하세요.")
        response = input("\n인증 후 계속하시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            return
        # 다시 확인
        auth_check = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, encoding='utf-8')
        if auth_check.returncode != 0:
            print("❌ 여전히 인증되지 않았습니다. 인증 후 다시 실행하세요.")
            return
    
    print("✅ GitHub CLI 인증 확인됨\n")
    print("실제 이슈 생성을 시작합니다...\n")
    
    # 사용자 확인
    response = input("계속하시겠습니까? (y/n): ")
    if response.lower() != 'y':
        print("취소되었습니다.")
        return
    
    # 이슈 생성 결과 저장
    issue_index = []
    
    # 각 파일에 대해 이슈 생성
    for md_file in md_files:
        filepath = Path(md_file)
        print(f"\n처리 중: {md_file}")
        
        try:
            title, body, issue_type, key = parse_markdown_file(filepath)
            labels = get_labels(issue_type)
            
            print(f"  Key: {key}, Type: {issue_type}, Labels: {', '.join(labels)}")
            
            issue_number, issue_url = create_github_issue(title, body, labels, key)
            
            if issue_number:
                print(f"  ✅ 이슈 생성 완료: #{issue_number} - {issue_url}")
                issue_index.append({
                    'key': key,
                    'issue_number': issue_number,
                    'title': title,
                    'url': issue_url,
                    'type': issue_type
                })
            else:
                print(f"  ❌ 이슈 생성 실패")
                issue_index.append({
                    'key': key,
                    'issue_number': None,
                    'title': title,
                    'url': None,
                    'type': issue_type,
                    'error': '생성 실패'
                })
        except Exception as e:
            print(f"  ❌ 오류 발생: {str(e)}")
            issue_index.append({
                'key': key if 'key' in locals() else 'UNKNOWN',
                'issue_number': None,
                'title': title if 'title' in locals() else 'UNKNOWN',
                'url': None,
                'type': issue_type if 'issue_type' in locals() else 'UNKNOWN',
                'error': str(e)
            })
    
    # 인덱스 파일 생성
    print("\n" + "=" * 80)
    print("이슈 인덱스 파일 생성 중...")
    
    # docs 디렉토리 생성
    docs_dir = Path('../docs')
    docs_dir.mkdir(exist_ok=True)
    
    # 마크다운 인덱스 파일 생성
    index_file = docs_dir / 'issue-index-backend.md'
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# Backend GitHub Issues Index\n\n")
        f.write("이 문서는 백엔드 GitHub Issues와 Task Key의 매핑을 제공합니다.\n\n")
        f.write("| Key | Issue # | Title | Type | URL |\n")
        f.write("|-----|---------|-------|------|-----|\n")
        
        for item in issue_index:
            issue_num = f"#{item['issue_number']}" if item['issue_number'] else "N/A"
            url = f"[링크]({item['url']})" if item['url'] else "N/A"
            title_short = item['title'][:50] + "..." if len(item['title']) > 50 else item['title']
            f.write(f"| {item['key']} | {issue_num} | {title_short} | {item['type']} | {url} |\n")
        
        f.write("\n## 통계\n\n")
        f.write(f"- 총 Task 수: {len(issue_index)}\n")
        f.write(f"- 생성 성공: {sum(1 for item in issue_index if item['issue_number'])}\n")
        f.write(f"- 생성 실패: {sum(1 for item in issue_index if not item['issue_number'])}\n")
    
    print(f"✅ 인덱스 파일 생성 완료: {index_file}")
    print(f"\n생성된 이슈 수: {sum(1 for item in issue_index if item['issue_number'])}/{len(issue_index)}")

if __name__ == '__main__':
    main()

