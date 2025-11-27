#!/bin/bash
# GitHub Issues에 Gantt 차트 일정 정보를 반영하는 스크립트
# 이 스크립트는 각 Issue에 Project를 추가하고 Date 필드를 설정합니다.

echo "=========================================="
echo "GitHub Issues에 Gantt 일정 정보 반영"
echo "=========================================="
echo ""

# 현재 날짜 설정 (Status 결정용)
CURRENT_DATE=$(date +%Y-%m-%d)
echo "현재 날짜: $CURRENT_DATE"
echo ""

# Issue별 Project 추가 및 Date 설정
# 형식: gh issue edit ISSUE_NUMBER --add-project PROJECT_NAME

# Prerequisites Lane
gh issue edit 16 --add-project reacademix-backend  # BE-INFRA-001
gh issue edit 17 --add-project reacademix-backend  # BE-INFRA-002
gh issue edit 18 --add-project reacademix-backend  # BE-INFRA-003
gh issue edit 4 --add-project reacademix-backend   # BE-COMMON-001
gh issue edit 5 --add-project reacademix-backend   # BE-COMMON-002
gh issue edit 6 --add-project reacademix-backend   # BE-COMMON-003

# Backend Core Lane
gh issue edit 1 --add-project reacademix-backend   # BE-AUTH-001
gh issue edit 2 --add-project reacademix-backend   # BE-AUTH-002
gh issue edit 3 --add-project reacademix-backend   # BE-AUTH-003
gh issue edit 38 --add-project reacademix-backend  # BE-STUDENT-001
gh issue edit 39 --add-project reacademix-backend  # BE-STUDENT-002
gh issue edit 20 --add-project reacademix-backend  # BE-INTEGRATION-001
gh issue edit 21 --add-project reacademix-backend  # BE-INTEGRATION-002
gh issue edit 22 --add-project reacademix-backend  # BE-INTEGRATION-003
gh issue edit 23 --add-project reacademix-backend  # BE-INTEGRATION-004
gh issue edit 24 --add-project reacademix-backend  # BE-INTEGRATION-005
gh issue edit 25 --add-project reacademix-backend  # BE-INTEGRATION-006
gh issue edit 26 --add-project reacademix-backend  # BE-INTEGRATION-007
gh issue edit 30 --add-project reacademix-backend  # BE-REPORT-001
gh issue edit 31 --add-project reacademix-backend  # BE-REPORT-002
gh issue edit 32 --add-project reacademix-backend  # BE-REPORT-003
gh issue edit 33 --add-project reacademix-backend  # BE-REPORT-004
gh issue edit 34 --add-project reacademix-backend  # BE-REPORT-005
gh issue edit 35 --add-project reacademix-backend  # BE-REPORT-006
gh issue edit 36 --add-project reacademix-backend  # BE-REPORT-007
gh issue edit 14 --add-project reacademix-backend  # BE-EMAIL-001
gh issue edit 15 --add-project reacademix-backend  # BE-EMAIL-002
gh issue edit 12 --add-project reacademix-backend  # BE-DELIVERY-001
gh issue edit 13 --add-project reacademix-backend  # BE-DELIVERY-002

# AI Engine Lane
gh issue edit 19 --add-project reacademix-backend  # BE-INSIGHT-001

# Financial Lane
gh issue edit 7 --add-project reacademix-backend   # BE-DATA-001
gh issue edit 8 --add-project reacademix-backend   # BE-DATA-002
gh issue edit 9 --add-project reacademix-backend   # BE-DATA-003
gh issue edit 10 --add-project reacademix-backend  # BE-DATA-004
gh issue edit 11 --add-project reacademix-backend  # BE-DATA-005

# NFR Lane
gh issue edit 37 --add-project reacademix-backend  # BE-SECURITY-001
gh issue edit 27 --add-project reacademix-backend  # BE-PERF-001
gh issue edit 28 --add-project reacademix-backend  # BE-PERF-002
gh issue edit 29 --add-project reacademix-backend  # BE-PERF-003

echo ""
echo "=========================================="
echo "완료!"
echo "=========================================="
echo ""
echo "참고: GitHub Projects의 Date 필드는 웹 UI에서 수동으로 설정하거나"
echo "Projects API를 사용해야 합니다. Issue 본문에는 Timeline 정보가"
echo "추가되었으므로 이를 참고하여 설정하세요."
echo ""

