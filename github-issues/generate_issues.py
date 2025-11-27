import json
import os
import re

def to_kebab_case(text):
    """한글 제목을 kebab-case로 변환 (공백을 하이픈으로)"""
    # 특수문자 제거 또는 변환
    text = text.replace('(', '').replace(')', '').replace('/', '-').replace('\\', '-')
    # 공백을 하이픈으로 변환
    text = text.replace(' ', '-')
    # 여러 하이픈을 하나로
    text = re.sub(r'-+', '-', text)
    # 앞뒤 하이픈 제거
    text = text.strip('-')
    return text

def get_technical_notes(task):
    """Technical Notes 생성"""
    notes = []
    
    # Controller/Service/Repository 추론
    if 'Controller' in task['description'] or 'API' in task['title']:
        notes.append("- Controller 레이어")
    if 'Service' in task['description'] or '서비스' in task['title']:
        notes.append("- Service 레이어")
    if 'Repository' in task['description'] or '데이터베이스' in task['description']:
        notes.append("- Repository 레이어")
    
    # DTO 추론
    if 'Dto' in str(task['acceptance_criteria']):
        notes.append("- DTO 클래스")
    
    # 엔티티/테이블 추론
    entities = []
    if 'User' in str(task['acceptance_criteria']):
        entities.append("User")
    if 'Student' in str(task['acceptance_criteria']):
        entities.append("Student")
    if 'Attendance' in str(task['acceptance_criteria']):
        entities.append("Attendance")
    if 'StudyTime' in str(task['acceptance_criteria']):
        entities.append("StudyTime")
    if 'MockExam' in str(task['acceptance_criteria']):
        entities.append("MockExam")
    if 'Assignment' in str(task['acceptance_criteria']):
        entities.append("Assignment")
    if 'Report' in str(task['acceptance_criteria']):
        entities.append("Report")
    if 'ReportDelivery' in str(task['acceptance_criteria']):
        entities.append("ReportDelivery")
    
    if entities:
        notes.append(f"- 관련 엔티티: {', '.join(entities)}")
    
    # 테이블 이름 추론
    tables = []
    if 'users 테이블' in str(task['acceptance_criteria']):
        tables.append("users")
    if 'students 테이블' in str(task['acceptance_criteria']):
        tables.append("students")
    if 'attendance 테이블' in str(task['acceptance_criteria']):
        tables.append("attendance")
    if 'study_time 테이블' in str(task['acceptance_criteria']):
        tables.append("study_time")
    if 'mock_exam 테이블' in str(task['acceptance_criteria']):
        tables.append("mock_exam")
    if 'assignments 테이블' in str(task['acceptance_criteria']):
        tables.append("assignments")
    if 'reports 테이블' in str(task['acceptance_criteria']):
        tables.append("reports")
    if 'report_delivery 테이블' in str(task['acceptance_criteria']):
        tables.append("report_delivery")
    
    if tables:
        notes.append(f"- 관련 테이블: {', '.join(tables)}")
    
    if not notes:
        notes.append("- 구현 세부사항은 acceptance criteria 참조")
    
    return '\n'.join(notes)

def generate_markdown(task):
    """Task를 마크다운 형식으로 변환"""
    # 파일명 생성
    filename = f"{task['key']}-{to_kebab_case(task['title'])}.md"
    
    # Type 변환
    type_display = "Functional" if task['type'] == "Functional" else "Non-Functional"
    if task['type'] == "Infrastructure":
        type_display = "Infrastructure"
    
    # REQ/Epic
    req_epic = task['req_id'] if task['req_id'] else task['epic']
    
    # Dependencies
    deps = ', '.join(task['dependencies']) if task['dependencies'] else 'None'
    
    # Acceptance Criteria
    ac_list = '\n'.join([f"- [ ] {ac}" for ac in task['acceptance_criteria']])
    
    # Technical Notes
    tech_notes = get_technical_notes(task)
    
    # Traceability
    traceability = f"- Related SRS: {task['req_id'] if task['req_id'] else 'N/A'}\n"
    traceability += f"- Related Epic: {task['epic']}"
    
    # 마크다운 템플릿
    markdown = f"""# {task['title']}

- **Type**: {type_display}
- **Key**: {task['key']}
- **REQ / Epic**: {req_epic}
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: {deps}

## 📌 Description

{task['description']}

## ✅ Acceptance Criteria

{ac_list}

## 🧩 Technical Notes

{tech_notes}

## 🔗 Traceability

{traceability}
"""
    
    return filename, markdown

# JSON 파일 읽기
with open('backend-tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# 파일 생성
created_files = []
for task in tasks:
    filename, markdown = generate_markdown(task)
    filepath = os.path.join('.', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    created_files.append(filename)
    print(f"Created: {filename}")

print(f"\n총 {len(created_files)}개 파일 생성 완료!")

