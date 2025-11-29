# API 응답 시간 최적화

- **Type**: Non-Functional
- **Key**: BE-PERF-003
- **REQ / Epic**: REQ-NF-005
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-COMMON-002

## 📌 Description

API 응답 시간을 최적화하여 평균 500ms 이내로 유지합니다.

## ✅ Acceptance Criteria

### 쿼리 최적화
- [ ] N+1 쿼리 문제 해결
- [ ] 필요한 인덱스 생성
- [ ] JOIN FETCH 적용

### 캐싱
- [ ] 자주 조회되는 데이터 캐싱 고려
- [ ] 캐시 무효화 전략 수립

### 모니터링
- [ ] 응답 시간 모니터링
- [ ] 느린 쿼리 로깅

### 테스트
- [ ] 성능 테스트 작성

---

## 💻 구현 코드

### 인덱스 생성 (Flyway Migration)

```sql
-- V3__add_performance_indexes.sql

-- 학생 검색용 인덱스
CREATE INDEX idx_student_name ON students(name);
CREATE INDEX idx_student_code ON students(student_code);
CREATE INDEX idx_student_class ON students(class_id);

-- 출석 데이터 조회용 인덱스
CREATE INDEX idx_attendance_student_date ON attendance(student_id, attendance_date);

-- 학습 시간 조회용 인덱스
CREATE INDEX idx_studytime_student_date ON study_time(student_id, study_date);

-- 모의고사 조회용 인덱스
CREATE INDEX idx_mockexam_student_date ON mock_exam(student_id, exam_date);

-- 리포트 조회용 인덱스
CREATE INDEX idx_report_student_status ON reports(student_id, status);
CREATE INDEX idx_report_created_at ON reports(created_at DESC);
```

### application.properties (JPA 최적화)

```properties
# JPA Performance Optimization
spring.jpa.properties.hibernate.default_batch_fetch_size=100
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true

# 쿼리 로깅 (개발 환경)
spring.jpa.properties.hibernate.generate_statistics=true
logging.level.org.hibernate.stat=DEBUG
```

### StudentRepository.java (최적화된 쿼리)

```java
@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {

    // JOIN FETCH로 N+1 방지
    @Query("""
        SELECT s FROM Student s
        LEFT JOIN FETCH s.classroom
        WHERE s.name LIKE %:name%
        """)
    List<Student> searchByName(@Param("name") String name);

    // 페이지네이션 시 카운트 쿼리 분리
    @Query(value = "SELECT s FROM Student s LEFT JOIN FETCH s.classroom WHERE s.classroom.id = :classId",
           countQuery = "SELECT COUNT(s) FROM Student s WHERE s.classroom.id = :classId")
    Page<Student> findByClassIdWithClassroom(@Param("classId") Long classId, Pageable pageable);
}
```

### PerformanceLoggingAspect.java

```java
@Aspect
@Component
@Slf4j
public class PerformanceLoggingAspect {

    private static final long SLOW_QUERY_THRESHOLD_MS = 500;

    @Around("@annotation(org.springframework.web.bind.annotation.GetMapping) || " +
            "@annotation(org.springframework.web.bind.annotation.PostMapping)")
    public Object logPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();

        try {
            return joinPoint.proceed();
        } finally {
            long duration = System.currentTimeMillis() - startTime;

            if (duration > SLOW_QUERY_THRESHOLD_MS) {
                log.warn("Slow API detected: {} - {}ms", 
                    joinPoint.getSignature().getName(), duration);
            }
        }
    }
}
```

---

## 📊 성능 목표

| API | 목표 응답 시간 | 최적화 전략 |
|-----|--------------|------------|
| 학생 검색 | ≤ 300ms | 인덱스 + 페이지네이션 |
| 학생 상세 | ≤ 200ms | JOIN FETCH |
| 리포트 목록 | ≤ 400ms | 인덱스 + 캐싱 |
| 대시보드 | ≤ 500ms | 병렬 쿼리 + 캐싱 |

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-04
- **End**: 2025-12-08
- **Lane**: NFR

## 🔗 Traceability

- Related SRS: REQ-NF-005
- Related Epic: Performance
