# 파일 업로드 데이터 수집 API 구현

- **Type**: Functional
- **Key**: BE-INTEGRATION-003
- **REQ / Epic**: REQ-FUNC-015
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-AUTH-002, BE-INTEGRATION-001, BE-INTEGRATION-002

## 📌 Description

CSV/Excel 파일을 업로드하여 데이터를 수집하는 API를 구현합니다.

## ✅ Acceptance Criteria

- [ ] POST /api/integrations/upload 엔드포인트 구현
- [ ] UploadFileRequestDto 클래스 생성 (file, systemType 필드)
- [ ] UploadFileResponseDto 클래스 생성 (uploadId, status, errors 필드)
- [ ] ValidationErrorDto 클래스 생성
- [ ] IntegrationsController.uploadFile() 메서드 구현
- [ ] FormData 파싱 (MultipartFile)
- [ ] 파일 업로드 서비스 호출
- [ ] 데이터 검증 서비스 호출
- [ ] 검증 오류 수집
- [ ] 파일 형식 검증
- [ ] 파일 크기 검증
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

## 🧩 Technical Notes

- Controller 레이어
- DTO 클래스


## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-18
- **Lane**: Backend Core
## 🔗 Traceability

- Related SRS: REQ-FUNC-015
- Related Epic: Data Integration
