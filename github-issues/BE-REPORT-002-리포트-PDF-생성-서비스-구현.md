# 리포트 PDF 생성 서비스 구현

- **Type**: Functional
- **Key**: BE-REPORT-002
- **REQ / Epic**: REQ-FUNC-009
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-REPORT-001

## 📌 Description

렌더링된 HTML을 PDF로 변환하는 서비스를 구현합니다. iText 또는 Apache PDFBox를 사용하여 PDF를 생성하고, 파일 저장소에 저장합니다.

## ✅ Acceptance Criteria

- [ ] PDF 생성 라이브러리 의존성 추가 (iText 또는 Apache PDFBox)
- [ ] ReportPdfService.generatePdf() 메서드 구현
- [ ] HTML을 PDF로 변환
- [ ] A4 용지 기준 PDF 생성
- [ ] 기본 정보, 그래프 및 차트 포함
- [ ] 파일 저장소에 PDF 파일 저장 (로컬 또는 클라우드 스토리지)
- [ ] 다운로드 URL 생성 및 반환
- [ ] PDF 생성 실패 시 에러 반환
- [ ] PDF 생성 시간 30초 이내 (REQ-NF-001)
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어
- 관련 엔티티: Report


## ⏱ 일정(Timeline)

- **Start**: 2025-12-04
- **End**: 2025-12-08
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-009
- Related Epic: Report Generation
