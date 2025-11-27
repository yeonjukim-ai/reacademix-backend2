# GitHub Issues 및 Projects 자동 동기화 스크립트
# 이 스크립트는 모든 Issue 파일을 업데이트하고 GitHub에 반영합니다.

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Issues 및 Projects 자동 동기화" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Task 정보 정의
$tasks = @(
    @{Task='BE-INFRA-001'; Issue=16; Start='2025-11-27'; End='2025-11-29'; Lane='Prerequisites'},
    @{Task='BE-INFRA-002'; Issue=17; Start='2025-11-30'; End='2025-12-03'; Lane='Prerequisites'},
    @{Task='BE-INFRA-003'; Issue=18; Start='2025-12-04'; End='2025-12-07'; Lane='Prerequisites'},
    @{Task='BE-COMMON-001'; Issue=4; Start='2025-11-30'; End='2025-12-02'; Lane='Prerequisites'},
    @{Task='BE-COMMON-002'; Issue=5; Start='2025-11-30'; End='2025-12-03'; Lane='Prerequisites'},
    @{Task='BE-COMMON-003'; Issue=6; Start='2025-11-30'; End='2025-12-02'; Lane='Prerequisites'},
    @{Task='BE-AUTH-001'; Issue=1; Start='2025-12-08'; End='2025-12-11'; Lane='Backend Core'},
    @{Task='BE-AUTH-002'; Issue=2; Start='2025-12-12'; End='2025-12-14'; Lane='Backend Core'},
    @{Task='BE-AUTH-003'; Issue=3; Start='2025-12-15'; End='2025-12-16'; Lane='Backend Core'},
    @{Task='BE-STUDENT-001'; Issue=38; Start='2025-12-15'; End='2025-12-17'; Lane='Backend Core'},
    @{Task='BE-STUDENT-002'; Issue=39; Start='2025-12-15'; End='2025-12-17'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-001'; Issue=20; Start='2025-11-30'; End='2025-12-04'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-002'; Issue=21; Start='2025-11-30'; End='2025-12-03'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-003'; Issue=22; Start='2025-12-15'; End='2025-12-18'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-004'; Issue=23; Start='2025-12-08'; End='2025-12-12'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-005'; Issue=24; Start='2025-12-13'; End='2025-12-15'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-006'; Issue=25; Start='2025-12-08'; End='2025-12-11'; Lane='Backend Core'},
    @{Task='BE-INTEGRATION-007'; Issue=26; Start='2025-12-15'; End='2025-12-17'; Lane='Backend Core'},
    @{Task='BE-REPORT-001'; Issue=30; Start='2025-11-30'; End='2025-12-03'; Lane='Backend Core'},
    @{Task='BE-REPORT-002'; Issue=31; Start='2025-12-04'; End='2025-12-08'; Lane='Backend Core'},
    @{Task='BE-REPORT-003'; Issue=32; Start='2025-12-19'; End='2025-12-24'; Lane='Backend Core'},
    @{Task='BE-REPORT-004'; Issue=33; Start='2025-12-25'; End='2025-12-27'; Lane='Backend Core'},
    @{Task='BE-REPORT-005'; Issue=34; Start='2025-12-25'; End='2025-12-26'; Lane='Backend Core'},
    @{Task='BE-REPORT-006'; Issue=35; Start='2025-12-25'; End='2025-12-27'; Lane='Backend Core'},
    @{Task='BE-REPORT-007'; Issue=36; Start='2025-12-27'; End='2025-12-29'; Lane='Backend Core'},
    @{Task='BE-EMAIL-001'; Issue=14; Start='2025-12-09'; End='2025-12-12'; Lane='Backend Core'},
    @{Task='BE-EMAIL-002'; Issue=15; Start='2025-12-25'; End='2025-12-28'; Lane='Backend Core'},
    @{Task='BE-DELIVERY-001'; Issue=12; Start='2025-12-08'; End='2025-12-09'; Lane='Backend Core'},
    @{Task='BE-DELIVERY-002'; Issue=13; Start='2025-12-15'; End='2025-12-17'; Lane='Backend Core'},
    @{Task='BE-INSIGHT-001'; Issue=19; Start='2025-12-12'; End='2025-12-16'; Lane='AI Engine'},
    @{Task='BE-DATA-001'; Issue=7; Start='2025-12-08'; End='2025-12-11'; Lane='Financial'},
    @{Task='BE-DATA-002'; Issue=8; Start='2025-12-08'; End='2025-12-11'; Lane='Financial'},
    @{Task='BE-DATA-003'; Issue=9; Start='2025-12-08'; End='2025-12-11'; Lane='Financial'},
    @{Task='BE-DATA-004'; Issue=10; Start='2025-12-08'; End='2025-12-11'; Lane='Financial'},
    @{Task='BE-DATA-005'; Issue=11; Start='2025-12-08'; End='2025-12-10'; Lane='Financial'},
    @{Task='BE-SECURITY-001'; Issue=37; Start='2025-12-08'; End='2025-12-12'; Lane='NFR'},
    @{Task='BE-PERF-001'; Issue=27; Start='2025-12-25'; End='2025-12-29'; Lane='NFR'},
    @{Task='BE-PERF-002'; Issue=28; Start='2025-12-25'; End='2025-12-29'; Lane='NFR'},
    @{Task='BE-PERF-003'; Issue=29; Start='2025-12-04'; End='2025-12-08'; Lane='NFR'}
)

Write-Host "Step 1: Issue 파일 업데이트 중..." -ForegroundColor Yellow
$updatedFiles = 0

foreach ($task in $tasks) {
    $files = Get-ChildItem -Path . -Filter "$($task.Task)-*.md"
    if ($files) {
        $file = $files[0]
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        $timeline = "`n## ⏱ 일정(Timeline)`n`n- **Start**: $($task.Start)`n- **End**: $($task.End)`n- **Lane**: $($task.Lane)`n"
        
        if ($content -match '## ⏱[️]? 일정\(Timeline\)') {
            $content = $content -replace '## ⏱[️]? 일정\(Timeline\).*?(?=\n## |\Z)', $timeline.Trim()
        } elseif ($content -match '## 🔗 Traceability') {
            $content = $content -replace '## 🔗 Traceability', "$timeline`n## 🔗 Traceability"
        } else {
            $content += $timeline
        }
        
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        $updatedFiles++
        Write-Host "  ✓ $($task.Task)" -ForegroundColor Green
    }
}

Write-Host "`n✅ $updatedFiles 개 파일 업데이트 완료`n" -ForegroundColor Green

Write-Host "Step 2: GitHub Issues 및 Projects 동기화 중..." -ForegroundColor Yellow
Write-Host ""

$successBody = 0
$successProject = 0
$failed = @()

foreach ($task in $tasks) {
    $files = Get-ChildItem -Path . -Filter "$($task.Task)-*.md"
    if ($files) {
        $file = $files[0]
        Write-Host "[$($task.Task)] Issue #$($task.Issue) " -NoNewline
        
        # 본문 업데이트
        $result = gh issue edit $task.Issue --body-file $file.FullName 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "본문✓ " -NoNewline -ForegroundColor Green
            $successBody++
        } else {
            Write-Host "본문✗ " -NoNewline -ForegroundColor Red
            $failed += "$($task.Task) 본문"
        }
        
        # Project 추가
        $result = gh issue edit $task.Issue --add-project reacademix-backend 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Project✓" -ForegroundColor Green
            $successProject++
        } else {
            Write-Host "Project✗" -ForegroundColor Red
            $failed += "$($task.Task) Project"
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "결과 요약" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "본문 업데이트: $successBody/$($tasks.Count) 성공" -ForegroundColor $(if ($successBody -eq $tasks.Count) { "Green" } else { "Yellow" })
Write-Host "Project 추가: $successProject/$($tasks.Count) 성공" -ForegroundColor $(if ($successProject -eq $tasks.Count) { "Green" } else { "Yellow" })
if ($failed.Count -gt 0) {
    Write-Host "실패: $($failed.Count)개" -ForegroundColor Red
    Write-Host "실패한 항목:" -ForegroundColor Red
    foreach ($item in $failed) {
        Write-Host "  - $item" -ForegroundColor Red
    }
}
Write-Host "`n참고: GitHub Projects의 Date 필드는 웹 UI에서 수동으로 설정하세요." -ForegroundColor Yellow
Write-Host ""

