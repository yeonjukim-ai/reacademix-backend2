# 학생 상세 정보 조회 API 구현

- **Type**: Functional
- **Key**: BE-STUDENT-002
- **REQ / Epic**: REQ-FUNC-001
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-AUTH-002, BE-INFRA-003

## 📌 Description

학생 ID로 학생의 상세 정보를 조회하는 API를 구현합니다. 리포트 생성 전 학생 정보 확인 및 학부모 연락처 확인에 사용됩니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `GET /api/v1/students/{studentId}` 엔드포인트 구현
- [ ] Path Variable로 studentId 처리
- [ ] 학생 상세 정보 반환

### DTO 클래스
- [ ] `StudentDetailDto` 클래스 생성 (기본 정보 + 추가 정보)

### 비즈니스 로직
- [ ] 학생 ID로 조회
- [ ] 존재하지 않는 studentId 시 404 반환
- [ ] 비활성 학생도 조회 가능 (status 포함)

### 성능 및 테스트
- [ ] API 응답 시간 500ms 이내
- [ ] 인증 토큰 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

---

## 📋 API 명세서

### 1. Endpoint

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **URI** | `/api/v1/students/{studentId}` |
| **Content-Type** | `application/json` |
| **인증 필요** | ✅ (JWT 토큰 필수) |

### 2. Path Variable

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `studentId` | Long | ✅ | 학생 ID |

**요청 예시:**
```http
GET /api/v1/students/1 HTTP/1.1
Host: api.reacademix.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Response Body

#### 3.1 성공 응답 (200 OK)

```json
{
  "success": true,
  "data": {
    "id": 1,
    "studentCode": "STU-2025-001",
    "name": "김철수",
    "className": "수능반A",
    "phone": "010-1234-5678",
    "parentPhone": "010-8765-4321",
    "parentEmail": "parent@test.com",
    "status": "ACTIVE",
    "enrollmentDate": "2025-03-01",
    "createdAt": "2025-03-01T09:00:00",
    "updatedAt": "2025-03-01T09:00:00"
  },
  "message": null
}
```

#### 3.2 실패 응답

| HTTP Status | 에러 코드 | 메시지 | 발생 조건 |
|-------------|----------|--------|----------|
| `401 Unauthorized` | `AUTH_001` | "인증 토큰이 필요합니다." | 토큰 없음 |
| `404 Not Found` | `RESOURCE_002` | "학생 정보를 찾을 수 없습니다." | 학생 없음 |

---

## 🔄 Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Controller as StudentController
    participant Service as StudentService
    participant Repo as StudentRepository
    participant DB as MySQL Database

    Client->>+Filter: GET /api/v1/students/1
    
    Note over Filter: JWT 토큰 검증
    Filter->>Controller: 인증 완료
    
    Controller->>+Service: getStudentById(1)
    Service->>+Repo: findById(1)
    Repo->>+DB: SELECT * FROM students WHERE id = 1
    
    alt 학생 존재
        DB-->>-Repo: Student record
        Repo-->>-Service: Optional<Student>
        Service->>Service: Entity → DTO 변환
        Service-->>-Controller: StudentDetailDto
        Controller-->>-Client: HTTP 200 OK
    else 학생 없음
        DB-->>Repo: Empty result
        Repo-->>Service: Optional.empty()
        Service-->>Controller: throw ResourceNotFoundException
        Controller-->>Client: HTTP 404 Not Found
    end
```

---

## 💻 ORM 예제 코드

### StudentDetailDto.java

```java
package com.reacademix.reacademix_backend.dto.response;

import com.reacademix.reacademix_backend.domain.student.Student;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 학생 상세 정보 DTO
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentDetailDto {

    private Long id;
    private String studentCode;
    private String name;
    private String className;
    private String phone;
    private String parentPhone;
    private String parentEmail;
    private String status;
    private LocalDate enrollmentDate;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static StudentDetailDto from(Student student) {
        return StudentDetailDto.builder()
            .id(student.getId())
            .studentCode(student.getStudentCode())
            .name(student.getName())
            .className(student.getClassName())
            .phone(student.getPhone())
            .parentPhone(student.getParentPhone())
            .parentEmail(student.getParentEmail())
            .status(student.getStatus().name())
            .enrollmentDate(student.getEnrollmentDate())
            .createdAt(student.getCreatedAt())
            .updatedAt(student.getUpdatedAt())
            .build();
    }
}
```

### StudentController.java (추가)

```java
/**
 * 학생 상세 조회 API
 */
@GetMapping("/{studentId}")
@Operation(summary = "학생 상세 조회", description = "학생 ID로 상세 정보를 조회합니다.")
public ResponseEntity<ApiResponse<StudentDetailDto>> getStudent(
        @Parameter(description = "학생 ID")
        @PathVariable Long studentId) {
    
    log.info("학생 상세 조회 요청: studentId={}", studentId);
    
    StudentDetailDto response = studentService.getStudentDetail(studentId);
    
    return ResponseEntity.ok(ApiResponse.success(response));
}
```

### StudentService.java (추가)

```java
/**
 * 학생 상세 조회
 */
public StudentDetailDto getStudentDetail(Long studentId) {
    Student student = studentRepository.findById(studentId)
        .orElseThrow(() -> new ResourceNotFoundException(
            ErrorCode.RESOURCE_002, "Student", "id", studentId));
    
    return StudentDetailDto.from(student);
}
```

---

## 📝 구현 체크리스트

### 1단계: DTO
- [ ] `StudentDetailDto` 생성

### 2단계: Service
- [ ] `getStudentDetail()` 구현
- [ ] 예외 처리 (ResourceNotFoundException)

### 3단계: Controller
- [ ] `getStudent()` 엔드포인트 구현

### 4단계: 테스트
- [ ] 단위 테스트
- [ ] 통합 테스트

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-001
- Related Epic: Student Management
