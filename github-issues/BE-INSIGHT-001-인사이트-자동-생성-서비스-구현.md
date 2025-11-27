# 인사이트 자동 생성 서비스 구현

- **Type**: Functional
- **Key**: BE-INSIGHT-001
- **REQ / Epic**: REQ-FUNC-008
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-DATA-001, BE-DATA-002, BE-DATA-003, BE-DATA-004

## 📌 Description

템플릿 기반 규칙 엔진을 사용하여 인사이트를 자동 생성하는 서비스를 구현합니다. 학습 시간 변화, 출석률 변화, 성적 변화를 분석하여 최대 3개의 인사이트를 생성합니다.

## ✅ Acceptance Criteria

- [ ] InsightService.generateInsights() 메서드 구현
- [ ] 템플릿 기반 규칙 엔진 구현
- [ ] 학습 시간 변화 분석 (목표 대비 감소/증가 판단)
- [ ] 출석률 변화 분석 (하락/상승 판단)
- [ ] 성적 변화 분석 (향상/하락 판단)
- [ ] 최대 3개의 인사이트 텍스트 생성
- [ ] 인사이트 형식: "최근 N주간 학습 시간이 목표 대비 X% 감소했습니다"
- [ ] 학생 데이터 부족 시 기본 인사이트 반환
- [ ] 처리 시간 1초 이내
- [ ] 단위 테스트 작성

## 🧩 Technical Notes

- Service 레이어


## ⏱ 일정(Timeline)

- **Start**: 2025-12-12
- **End**: 2025-12-16
- **Lane**: AI Engine
## 🔗 Traceability

- Related SRS: REQ-FUNC-008
- Related Epic: Report Generation
