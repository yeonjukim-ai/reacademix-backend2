# PowerShell 스크립트: GitHub Issues 및 Projects 동기화
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "GitHub Issues 및 Projects 자동 동기화" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 모든 Issue에 Project 추가
$issues = @(
    @{Task='BE-INFRA-001'; Issue=16}, @{Task='BE-INFRA-002'; Issue=17}, @{Task='BE-INFRA-003'; Issue=18},
    @{Task='BE-COMMON-001'; Issue=4}, @{Task='BE-COMMON-002'; Issue=5}, @{Task='BE-COMMON-003'; Issue=6},
    @{Task='BE-AUTH-001'; Issue=1}, @{Task='BE-AUTH-002'; Issue=2}, @{Task='BE-AUTH-003'; Issue=3},
    @{Task='BE-STUDENT-001'; Issue=38}, @{Task='BE-STUDENT-002'; Issue=39},
    @{Task='BE-INTEGRATION-001'; Issue=20}, @{Task='BE-INTEGRATION-002'; Issue=21}, @{Task='BE-INTEGRATION-003'; Issue=22},
    @{Task='BE-INTEGRATION-004'; Issue=23}, @{Task='BE-INTEGRATION-005'; Issue=24}, @{Task='BE-INTEGRATION-006'; Issue=25}, @{Task='BE-INTEGRATION-007'; Issue=26},
    @{Task='BE-REPORT-001'; Issue=30}, @{Task='BE-REPORT-002'; Issue=31}, @{Task='BE-REPORT-003'; Issue=32},
    @{Task='BE-REPORT-004'; Issue=33}, @{Task='BE-REPORT-005'; Issue=34}, @{Task='BE-REPORT-006'; Issue=35}, @{Task='BE-REPORT-007'; Issue=36},
    @{Task='BE-EMAIL-001'; Issue=14}, @{Task='BE-EMAIL-002'; Issue=15},
    @{Task='BE-DELIVERY-001'; Issue=12}, @{Task='BE-DELIVERY-002'; Issue=13},
    @{Task='BE-INSIGHT-001'; Issue=19},
    @{Task='BE-DATA-001'; Issue=7}, @{Task='BE-DATA-002'; Issue=8}, @{Task='BE-DATA-003'; Issue=9}, @{Task='BE-DATA-004'; Issue=10}, @{Task='BE-DATA-005'; Issue=11},
    @{Task='BE-SECURITY-001'; Issue=37}, @{Task='BE-PERF-001'; Issue=27}, @{Task='BE-PERF-002'; Issue=28}, @{Task='BE-PERF-003'; Issue=29}
)

Write-Host "Step 1: GitHub Issues 본문 업데이트 및 Project 추가" -ForegroundColor Yellow
Write-Host ""

$successCount = 0
$failedCount = 0

foreach ($item in $issues) {
    $task = $item.Task
    $issueNum = $item.Issue
    
    Write-Host "[$task] Issue #$issueNum 처리 중... " -NoNewline
    
    # 파일 찾기
    $file = Get-ChildItem -Path . -Filter "$task-*.md" | Select-Object -First 1
    
    if ($file) {
        # 본문 업데이트
        try {
            gh issue edit $issueNum --body-file $file.FullName 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "본문✓ " -NoNewline -ForegroundColor Green
            } else {
                Write-Host "본문✗ " -NoNewline -ForegroundColor Red
                $failedCount++
            }
        } catch {
            Write-Host "본문✗ " -NoNewline -ForegroundColor Red
            $failedCount++
        }
        
        # Project 추가
        try {
            gh issue edit $issueNum --add-project reacademix-backend 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Project✓" -ForegroundColor Green
                $successCount++
            } else {
                Write-Host "Project✗" -ForegroundColor Red
                $failedCount++
            }
        } catch {
            Write-Host "Project✗" -ForegroundColor Red
            $failedCount++
        }
    } else {
        Write-Host "파일 없음" -ForegroundColor Yellow
        $failedCount++
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "결과 요약" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "성공: $successCount개" -ForegroundColor Green
Write-Host "실패: $failedCount개" -ForegroundColor $(if ($failedCount -gt 0) { "Red" } else { "Green" })
Write-Host ""
Write-Host "참고: GitHub Projects의 Date 필드는 웹 UI에서 수동으로 설정하세요." -ForegroundColor Yellow
Write-Host ""

