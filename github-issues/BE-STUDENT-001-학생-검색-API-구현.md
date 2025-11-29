# 학생 검색 API 구현

- **Type**: Functional
- **Key**: BE-STUDENT-001
- **REQ / Epic**: REQ-FUNC-001
- **Service**: ReAcademix Backend
- **Priority**: High
- **Dependencies**: BE-AUTH-002, BE-INFRA-003

## 📌 Description

학생 이름 또는 학생 ID로 학생을 검색하는 API를 구현합니다. 부분 일치 검색을 지원하고, 페이지네이션을 제공합니다. 리포트 생성을 위한 학생 선택 기능의 핵심 API입니다.

## ✅ Acceptance Criteria

### API 구현
- [ ] `GET /api/v1/students` 엔드포인트 구현
- [ ] 검색어 파라미터 처리 (`search`)
- [ ] 페이지네이션 파라미터 처리 (`page`, `size`)
- [ ] 반 필터링 파라미터 처리 (`className`)

### DTO 클래스
- [ ] `StudentSearchRequest` DTO 생성
- [ ] `StudentSearchResponse` DTO 생성
- [ ] `StudentDto` DTO 생성

### 비즈니스 로직
- [ ] 이름/학생코드 부분 일치 검색
- [ ] 검색 결과 최대 50명 제한
- [ ] 페이지네이션 기본값: page=0, size=20
- [ ] 활성 학생만 검색 (status=ACTIVE)
- [ ] 빈 검색어 시 전체 목록 반환

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
| **URI** | `/api/v1/students` |
| **Content-Type** | `application/json` |
| **인증 필요** | ✅ (JWT 토큰 필수) |

### 2. Request Parameters (Query String)

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `search` | String | ❌ | - | 검색어 (학생 이름 또는 학생 코드) |
| `className` | String | ❌ | - | 반 이름 필터 |
| `page` | Integer | ❌ | 0 | 페이지 번호 (0부터 시작) |
| `size` | Integer | ❌ | 20 | 페이지 크기 (최대 50) |

**요청 예시:**
```http
GET /api/v1/students?search=김철수&page=0&size=20 HTTP/1.1
Host: api.reacademix.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Response Body

#### 3.1 성공 응답 (200 OK)

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | Boolean | 요청 성공 여부 |
| `data` | Object | 응답 데이터 |
| `data.students` | Array | 학생 목록 |
| `data.students[].id` | Long | 학생 ID |
| `data.students[].studentCode` | String | 학생 코드 |
| `data.students[].name` | String | 학생 이름 |
| `data.students[].className` | String | 반 이름 |
| `data.students[].parentEmail` | String | 학부모 이메일 |
| `data.students[].status` | String | 학생 상태 |
| `data.pagination` | Object | 페이지네이션 정보 |
| `data.pagination.page` | Integer | 현재 페이지 |
| `data.pagination.size` | Integer | 페이지 크기 |
| `data.pagination.totalElements` | Long | 전체 데이터 수 |
| `data.pagination.totalPages` | Integer | 전체 페이지 수 |

**성공 응답 예시:**
```json
{
  "success": true,
  "data": {
    "students": [
      {
        "id": 1,
        "studentCode": "STU-2025-001",
        "name": "김철수",
        "className": "수능반A",
        "parentEmail": "parent1@test.com",
        "status": "ACTIVE"
      },
      {
        "id": 2,
        "studentCode": "STU-2025-002",
        "name": "김영희",
        "className": "수능반A",
        "parentEmail": "parent2@test.com",
        "status": "ACTIVE"
      }
    ],
    "pagination": {
      "page": 0,
      "size": 20,
      "totalElements": 2,
      "totalPages": 1
    }
  },
  "message": null
}
```

#### 3.2 실패 응답

| HTTP Status | 에러 코드 | 메시지 | 발생 조건 |
|-------------|----------|--------|----------|
| `401 Unauthorized` | `AUTH_001` | "인증 토큰이 필요합니다." | 토큰 없음 |
| `401 Unauthorized` | `AUTH_005` | "토큰이 만료되었습니다." | 토큰 만료 |
| `400 Bad Request` | `VALIDATION_001` | "입력 데이터 검증에 실패했습니다." | 파라미터 오류 |

---

## 📊 1. ERD (관련 엔티티)

```mermaid
erDiagram
    students {
        BIGINT id PK
        VARCHAR student_code UK "학생 코드"
        VARCHAR name "학생 이름"
        VARCHAR class_name "반 이름"
        VARCHAR phone "연락처"
        VARCHAR parent_phone "학부모 연락처"
        VARCHAR parent_email "학부모 이메일"
        VARCHAR status "ACTIVE, INACTIVE, GRADUATED"
        DATE enrollment_date "입학일"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
```

### 검색 쿼리 인덱스

| 인덱스명 | 컬럼 | 용도 |
|----------|------|------|
| `idx_students_name` | `name` | 이름 검색 |
| `idx_students_student_code` | `student_code` | 학생 코드 검색 |
| `idx_students_class_name` | `class_name` | 반 필터링 |
| `idx_students_status` | `status` | 상태 필터링 |

---

## 🔄 2. Sequence Diagram

### 2.1 학생 검색 성공 흐름

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Filter as JwtAuthenticationFilter
    participant Controller as StudentController
    participant Service as StudentService
    participant Repo as StudentRepository
    participant DB as MySQL Database

    Client->>+Filter: GET /api/v1/students?search=김철수
    
    Note over Filter: JWT 토큰 검증
    Filter->>Filter: validateToken() ✓
    Filter->>Controller: 인증 완료
    
    Controller->>Controller: @RequestParam 바인딩
    Controller->>+Service: searchStudents(search, page, size)
    
    Service->>Service: 검색 조건 생성
    Note over Service: search가 있으면<br/>이름/학생코드 LIKE 검색
    
    Service->>+Repo: searchByKeyword(keyword, pageable)
    Repo->>+DB: SELECT * FROM students<br/>WHERE (name LIKE '%김철수%'<br/>OR student_code LIKE '%김철수%')<br/>AND status = 'ACTIVE'<br/>LIMIT 20 OFFSET 0
    
    DB-->>-Repo: Student records
    Repo-->>-Service: Page<Student>
    
    Service->>Service: Entity → DTO 변환
    Service-->>-Controller: StudentSearchResponse
    
    Controller-->>-Client: HTTP 200 OK
    
    Note over Client: {<br/>"success": true,<br/>"data": {<br/>  "students": [...],<br/>  "pagination": {...}<br/>}<br/>}
```

### 2.2 빈 검색어 전체 조회

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant Controller as StudentController
    participant Service as StudentService
    participant Repo as StudentRepository
    participant DB as MySQL Database

    Client->>+Controller: GET /api/v1/students?page=0&size=20
    
    Controller->>+Service: searchStudents(null, 0, 20)
    
    Note over Service: search가 null/empty<br/>→ 전체 목록 조회
    
    Service->>+Repo: findByStatus(ACTIVE, pageable)
    Repo->>+DB: SELECT * FROM students<br/>WHERE status = 'ACTIVE'<br/>ORDER BY name ASC<br/>LIMIT 20 OFFSET 0
    
    DB-->>-Repo: Student records
    Repo-->>-Service: Page<Student>
    
    Service-->>-Controller: StudentSearchResponse
    Controller-->>-Client: HTTP 200 OK
```

---

## 🏛️ 3. CLD (Class Diagram)

```mermaid
classDiagram
    class StudentController {
        -StudentService studentService
        +searchStudents(search, className, page, size) ResponseEntity
    }
    
    class StudentService {
        -StudentRepository studentRepository
        +searchStudents(search, className, page, size) StudentSearchResponse
        -buildPageable(page, size) Pageable
    }
    
    class StudentRepository {
        <<interface>>
        +searchByKeyword(keyword, pageable) Page~Student~
        +findByStatus(status, pageable) Page~Student~
        +findByClassNameAndStatus(className, status, pageable) Page~Student~
    }
    
    class StudentSearchResponse {
        -List~StudentDto~ students
        -PaginationInfo pagination
        +of(Page~Student~) StudentSearchResponse
    }
    
    class StudentDto {
        -Long id
        -String studentCode
        -String name
        -String className
        -String parentEmail
        -String status
        +from(Student) StudentDto
    }
    
    class PaginationInfo {
        -int page
        -int size
        -long totalElements
        -int totalPages
    }
    
    StudentController --> StudentService
    StudentService --> StudentRepository
    StudentService --> StudentSearchResponse
    StudentSearchResponse --> StudentDto
    StudentSearchResponse --> PaginationInfo
```

---

## 💻 4. ORM 예제 코드

### 4.1 StudentSearchRequest.java

```java
package com.reacademix.reacademix_backend.dto.request;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 학생 검색 요청 DTO
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentSearchRequest {

    private String search;
    
    private String className;
    
    @Min(value = 0, message = "페이지 번호는 0 이상이어야 합니다.")
    @Builder.Default
    private Integer page = 0;
    
    @Min(value = 1, message = "페이지 크기는 1 이상이어야 합니다.")
    @Max(value = 50, message = "페이지 크기는 50 이하여야 합니다.")
    @Builder.Default
    private Integer size = 20;
}
```

### 4.2 StudentDto.java

```java
package com.reacademix.reacademix_backend.dto.response;

import com.reacademix.reacademix_backend.domain.student.Student;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 학생 정보 DTO
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentDto {

    private Long id;
    private String studentCode;
    private String name;
    private String className;
    private String parentEmail;
    private String status;

    /**
     * Entity → DTO 변환
     */
    public static StudentDto from(Student student) {
        return StudentDto.builder()
            .id(student.getId())
            .studentCode(student.getStudentCode())
            .name(student.getName())
            .className(student.getClassName())
            .parentEmail(student.getParentEmail())
            .status(student.getStatus().name())
            .build();
    }
}
```

### 4.3 StudentSearchResponse.java

```java
package com.reacademix.reacademix_backend.dto.response;

import com.reacademix.reacademix_backend.domain.student.Student;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.domain.Page;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 학생 검색 응답 DTO
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentSearchResponse {

    private List<StudentDto> students;
    private PaginationInfo pagination;

    /**
     * Page<Student> → StudentSearchResponse 변환
     */
    public static StudentSearchResponse of(Page<Student> studentPage) {
        List<StudentDto> students = studentPage.getContent()
            .stream()
            .map(StudentDto::from)
            .collect(Collectors.toList());
        
        PaginationInfo pagination = PaginationInfo.builder()
            .page(studentPage.getNumber())
            .size(studentPage.getSize())
            .totalElements(studentPage.getTotalElements())
            .totalPages(studentPage.getTotalPages())
            .build();
        
        return StudentSearchResponse.builder()
            .students(students)
            .pagination(pagination)
            .build();
    }

    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PaginationInfo {
        private int page;
        private int size;
        private long totalElements;
        private int totalPages;
    }
}
```

### 4.4 StudentRepository.java (검색 메서드 추가)

```java
package com.reacademix.reacademix_backend.repository;

import com.reacademix.reacademix_backend.domain.student.Student;
import com.reacademix.reacademix_backend.domain.student.StudentStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Student Repository
 */
@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {

    /**
     * 학생 코드로 조회
     */
    Optional<Student> findByStudentCode(String studentCode);

    /**
     * 키워드로 학생 검색 (이름 또는 학생코드 부분 일치)
     * 활성 학생만 검색
     */
    @Query("SELECT s FROM Student s " +
           "WHERE (s.name LIKE %:keyword% OR s.studentCode LIKE %:keyword%) " +
           "AND s.status = :status " +
           "ORDER BY s.name ASC")
    Page<Student> searchByKeyword(
        @Param("keyword") String keyword, 
        @Param("status") StudentStatus status,
        Pageable pageable);

    /**
     * 상태별 학생 목록 조회
     */
    Page<Student> findByStatusOrderByNameAsc(StudentStatus status, Pageable pageable);

    /**
     * 반 이름과 상태로 학생 검색
     */
    @Query("SELECT s FROM Student s " +
           "WHERE s.className = :className " +
           "AND s.status = :status " +
           "ORDER BY s.name ASC")
    Page<Student> findByClassNameAndStatus(
        @Param("className") String className,
        @Param("status") StudentStatus status,
        Pageable pageable);

    /**
     * 키워드와 반 이름으로 검색
     */
    @Query("SELECT s FROM Student s " +
           "WHERE (s.name LIKE %:keyword% OR s.studentCode LIKE %:keyword%) " +
           "AND s.className = :className " +
           "AND s.status = :status " +
           "ORDER BY s.name ASC")
    Page<Student> searchByKeywordAndClassName(
        @Param("keyword") String keyword,
        @Param("className") String className,
        @Param("status") StudentStatus status,
        Pageable pageable);
}
```

### 4.5 StudentService.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.student.Student;
import com.reacademix.reacademix_backend.domain.student.StudentStatus;
import com.reacademix.reacademix_backend.dto.response.StudentSearchResponse;
import com.reacademix.reacademix_backend.exception.ResourceNotFoundException;
import com.reacademix.reacademix_backend.repository.StudentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

/**
 * 학생 관련 비즈니스 로직 Service
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StudentService {

    private final StudentRepository studentRepository;
    
    private static final int MAX_PAGE_SIZE = 50;

    /**
     * 학생 검색
     * 
     * @param search 검색어 (이름 또는 학생코드)
     * @param className 반 이름 필터 (선택)
     * @param page 페이지 번호 (0부터 시작)
     * @param size 페이지 크기
     * @return StudentSearchResponse
     */
    public StudentSearchResponse searchStudents(String search, String className, int page, int size) {
        // 페이지 크기 제한
        int validSize = Math.min(size, MAX_PAGE_SIZE);
        Pageable pageable = PageRequest.of(page, validSize);
        
        Page<Student> studentPage;
        
        // 검색 조건에 따른 쿼리 분기
        boolean hasSearch = StringUtils.hasText(search);
        boolean hasClassName = StringUtils.hasText(className);
        
        if (hasSearch && hasClassName) {
            // 키워드 + 반 이름 검색
            studentPage = studentRepository.searchByKeywordAndClassName(
                search.trim(), className, StudentStatus.ACTIVE, pageable);
        } else if (hasSearch) {
            // 키워드만 검색
            studentPage = studentRepository.searchByKeyword(
                search.trim(), StudentStatus.ACTIVE, pageable);
        } else if (hasClassName) {
            // 반 이름만 필터
            studentPage = studentRepository.findByClassNameAndStatus(
                className, StudentStatus.ACTIVE, pageable);
        } else {
            // 전체 목록
            studentPage = studentRepository.findByStatusOrderByNameAsc(
                StudentStatus.ACTIVE, pageable);
        }
        
        log.debug("학생 검색 결과: search={}, className={}, total={}", 
            search, className, studentPage.getTotalElements());
        
        return StudentSearchResponse.of(studentPage);
    }

    /**
     * 학생 상세 조회
     * 
     * @param studentId 학생 ID
     * @return Student
     * @throws ResourceNotFoundException 학생이 없는 경우
     */
    public Student getStudentById(Long studentId) {
        return studentRepository.findById(studentId)
            .orElseThrow(() -> new ResourceNotFoundException("Student", "id", studentId));
    }
}
```

### 4.6 StudentController.java

```java
package com.reacademix.reacademix_backend.controller;

import com.reacademix.reacademix_backend.dto.response.ApiResponse;
import com.reacademix.reacademix_backend.dto.response.StudentSearchResponse;
import com.reacademix.reacademix_backend.service.StudentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * 학생 관련 REST API Controller
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/students")
@RequiredArgsConstructor
@Validated
@Tag(name = "Student", description = "학생 관리 API")
public class StudentController {

    private final StudentService studentService;

    /**
     * 학생 검색 API
     * 
     * @param search 검색어 (이름 또는 학생코드)
     * @param className 반 이름 필터
     * @param page 페이지 번호
     * @param size 페이지 크기
     * @return ResponseEntity<ApiResponse<StudentSearchResponse>>
     */
    @GetMapping
    @Operation(summary = "학생 검색", description = "학생 이름 또는 학생 코드로 검색합니다.")
    public ResponseEntity<ApiResponse<StudentSearchResponse>> searchStudents(
            @Parameter(description = "검색어 (이름 또는 학생코드)")
            @RequestParam(required = false) String search,
            
            @Parameter(description = "반 이름 필터")
            @RequestParam(required = false) String className,
            
            @Parameter(description = "페이지 번호 (0부터 시작)")
            @RequestParam(defaultValue = "0") @Min(0) Integer page,
            
            @Parameter(description = "페이지 크기 (최대 50)")
            @RequestParam(defaultValue = "20") @Min(1) @Max(50) Integer size) {
        
        log.info("학생 검색 요청: search={}, className={}, page={}, size={}", 
            search, className, page, size);
        
        StudentSearchResponse response = studentService.searchStudents(search, className, page, size);
        
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
```

---

## 🧪 5. 테스트 코드

### 5.1 StudentServiceTest.java

```java
package com.reacademix.reacademix_backend.service;

import com.reacademix.reacademix_backend.domain.student.Student;
import com.reacademix.reacademix_backend.domain.student.StudentStatus;
import com.reacademix.reacademix_backend.dto.response.StudentSearchResponse;
import com.reacademix.reacademix_backend.repository.StudentRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import java.util.Arrays;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;

@ExtendWith(MockitoExtension.class)
class StudentServiceTest {

    @Mock
    private StudentRepository studentRepository;

    @InjectMocks
    private StudentService studentService;

    @Test
    @DisplayName("검색어로 학생 검색 성공")
    void searchStudents_WithKeyword_Success() {
        // given
        List<Student> students = Arrays.asList(
            Student.builder().studentCode("STU-001").name("김철수").className("수능반A").build(),
            Student.builder().studentCode("STU-002").name("김영희").className("수능반A").build()
        );
        Page<Student> studentPage = new PageImpl<>(students);
        
        given(studentRepository.searchByKeyword(eq("김"), eq(StudentStatus.ACTIVE), any(Pageable.class)))
            .willReturn(studentPage);

        // when
        StudentSearchResponse response = studentService.searchStudents("김", null, 0, 20);

        // then
        assertThat(response.getStudents()).hasSize(2);
        assertThat(response.getPagination().getTotalElements()).isEqualTo(2);
    }

    @Test
    @DisplayName("빈 검색어로 전체 학생 조회 성공")
    void searchStudents_WithoutKeyword_ReturnsAll() {
        // given
        List<Student> students = Arrays.asList(
            Student.builder().studentCode("STU-001").name("김철수").build()
        );
        Page<Student> studentPage = new PageImpl<>(students);
        
        given(studentRepository.findByStatusOrderByNameAsc(eq(StudentStatus.ACTIVE), any(Pageable.class)))
            .willReturn(studentPage);

        // when
        StudentSearchResponse response = studentService.searchStudents(null, null, 0, 20);

        // then
        assertThat(response.getStudents()).hasSize(1);
    }
}
```

---

## 📝 구현 체크리스트

### 1단계: DTO 클래스 생성
- [ ] `StudentSearchRequest`
- [ ] `StudentDto`
- [ ] `StudentSearchResponse`
- [ ] `PaginationInfo`

### 2단계: Repository 메서드 추가
- [ ] `searchByKeyword()`
- [ ] `findByStatusOrderByNameAsc()`
- [ ] `findByClassNameAndStatus()`
- [ ] `searchByKeywordAndClassName()`

### 3단계: Service 구현
- [ ] `StudentService.searchStudents()` 구현
- [ ] 페이지 크기 제한 로직
- [ ] 검색 조건 분기 로직

### 4단계: Controller 구현
- [ ] `StudentController.searchStudents()` 구현
- [ ] Swagger 문서화
- [ ] 파라미터 검증

### 5단계: 테스트
- [ ] Service 단위 테스트
- [ ] Controller 통합 테스트
- [ ] 성능 테스트 (500ms 이내)

---

## ⏱ 일정(Timeline)

- **Start**: 2025-12-15
- **End**: 2025-12-17
- **Lane**: Backend Core

## 🔗 Traceability

- Related SRS: REQ-FUNC-001
- Related Epic: Student Management
- Next Tasks: BE-STUDENT-002, BE-REPORT-003
