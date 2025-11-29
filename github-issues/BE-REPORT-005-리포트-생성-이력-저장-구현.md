# 리포트 생성 이력 저장 구현

- **Type**: Functional
- **Key**: BE-REPORT-005
- **REQ / Epic**: REQ-FUNC-013
- **Service**: ReAcademix Backend
- **Priority**: Medium
- **Dependencies**: BE-INFRA-003, BE-REPORT-003

## 📌 Description

리포트 생성 이력을 데이터베이스에 저장하는 기능을 구현합니다. 생성 시간, 상태, 파일 경로 등을 기록합니다.

## ✅ Acceptance Criteria

### Entity 구현
- [ ] `Report` 엔티티에 이력 필드 추가
- [ ] 상태 변경 이력 추적

### Service 구현
- [ ] 생성 이력 저장 로직 구현
- [ ] 상태 업데이트 로직 구현

### 테스트
- [ ] 단위 테스트 작성

---

## 💻 구현 코드

### Report.java (이력 필드 포함)

```java
@Entity
@Table(name = "reports")
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Report extends BaseTimeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id", nullable = false)
    private Student student;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by", nullable = false)
    private User createdBy;

    @Column(name = "report_start_date", nullable = false)
    private LocalDate reportStartDate;

    @Column(name = "report_end_date", nullable = false)
    private LocalDate reportEndDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ReportStatus status;

    @Column(name = "file_path")
    private String filePath;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "insights", columnDefinition = "TEXT")
    private String insights;  // JSON 형식

    @Column(name = "generation_started_at")
    private LocalDateTime generationStartedAt;

    @Column(name = "generation_completed_at")
    private LocalDateTime generationCompletedAt;

    @Column(name = "generation_duration_ms")
    private Long generationDurationMs;

    @Column(name = "failure_reason")
    private String failureReason;

    @Column(name = "download_count")
    private int downloadCount = 0;

    @Column(name = "last_downloaded_at")
    private LocalDateTime lastDownloadedAt;

    // === 상태 변경 메서드 ===
    
    public void startGeneration() {
        this.status = ReportStatus.GENERATING;
        this.generationStartedAt = LocalDateTime.now();
    }

    public void markAsCompleted(String filePath, Long fileSize, String insights) {
        this.status = ReportStatus.COMPLETED;
        this.filePath = filePath;
        this.fileSize = fileSize;
        this.insights = insights;
        this.generationCompletedAt = LocalDateTime.now();
        this.generationDurationMs = Duration.between(
            generationStartedAt, generationCompletedAt).toMillis();
    }

    public void markAsFailed(String reason) {
        this.status = ReportStatus.FAILED;
        this.failureReason = reason;
        this.generationCompletedAt = LocalDateTime.now();
        if (generationStartedAt != null) {
            this.generationDurationMs = Duration.between(
                generationStartedAt, generationCompletedAt).toMillis();
        }
    }

    public void incrementDownloadCount() {
        this.downloadCount++;
        this.lastDownloadedAt = LocalDateTime.now();
    }
}
```

### ReportStatus.java

```java
public enum ReportStatus {
    PENDING,      // 생성 대기
    GENERATING,   // 생성 중
    COMPLETED,    // 완료
    FAILED        // 실패
}
```

### ReportRepository.java

```java
@Repository
public interface ReportRepository extends JpaRepository<Report, Long> {

    List<Report> findByStudentIdOrderByCreatedAtDesc(Long studentId);

    Page<Report> findByStudentId(Long studentId, Pageable pageable);

    @Query("SELECT r FROM Report r WHERE r.student.id = :studentId AND r.status = :status")
    List<Report> findByStudentIdAndStatus(
        @Param("studentId") Long studentId, 
        @Param("status") ReportStatus status);

    boolean existsByStudentIdAndStatus(Long studentId, ReportStatus status);

    @Query("SELECT r FROM Report r JOIN FETCH r.student WHERE r.id = :id")
    Optional<Report> findByIdWithStudent(@Param("id") Long id);
}
```

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-25
- **End**: 2025-12-26
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-013
- Related Epic: Report Generation
