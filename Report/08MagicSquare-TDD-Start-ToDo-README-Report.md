# Magic Square TDD Start — To-Do · README 준비 보고서

## 1) 목적

Magic Square 4x4 TDD Practice 프로젝트의 **구현 착수 전** 단계에서,
PRD·User Journey·Dual-Track TDD 설계를 바탕으로 다음 산출물을 정리·고정한다.

- 테스트 플랜 샘플 예제 1건 선정 (FR-01 선행 검증)
- Scenario → AC → RED → GREEN → REFACTOR 추적 개발 보드 (To-Do List)
- 프로젝트 시작 선언용 README.md 초안 (Markdown 본문, 미저장)

본 보고서는 **구현 코드·테스트 코드·파일 생성 없이** 기획·추적 구조만 확정한 결과를 기록한다.

## 2) 수행 범위

| 단계 | 내용 | 산출 |
|------|------|------|
| 1 | Report/ 기반 테스트 플랜 샘플 1건 선정 | AC-FR01-01 + `grid=None` + S-011 |
| 2 | 통합 개발 To-Do List (1차·2차) | 채팅 Markdown (Phase 0~7) |
| 3 | Dual-Track TDD 추적 보드 (정식) | TASK-001~021, Tracking Board 표 |
| 4 | README 시작 가이드 초안 | 10섹션 Markdown 본문 |
| 5 | Report·Transcript Export | 본 보고서, `Prompt/08` |

제외:

- `README.md` 루트 파일 덮어쓰기
- `tests/`·`entity/`·`boundary/` 마방진 구현
- RED 테스트 실행 및 GREEN 구현

## 3) 참고 문서 및 매핑

| 논리명 | 저장소 경로 | 본 세션 반영 |
|--------|-------------|--------------|
| PRD | `docs/PRD_MagicSquare.md` | FR-01~05, BR-01~14, §12~16, Error Catalog |
| Report/2 TDD Design | `Report/02MagicSquare-TDD-Design-Report.md` | I-1 선행, S-011 null 경계, D-4 검사 순서 |
| Report/4 User Journey | `Report/06MagicSquare-UserJourney-Story-Scenario-Report.md` | Story 1~5, SC-BND-VAL, SC-DOM-SOL-001 |
| Report/3 ECB | `Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md` | Boundary→Control→Entity, pytest |
| Report/7 PRD Review | `Report/07MagicSquare-PRD-Development-and-Review-Report.md` | TD-02/TD-07 OPEN, Matrix AC 누락 |

## 4) 테스트 플랜 샘플 예제 선정

### 4.1 선택 결과

| 항목 | 값 |
|------|-----|
| **Report 출처** | `Report/02` 시나리오 **S-011** (경계 입력 거부: null/빈 배열) |
| **선택 AC** | **AC-FR01-01** (입력 형태 비성립) |
| **PRD** | **FR-01**, §12.1, §13.2, §16.2 ES-01 |
| **입력** | `grid = None` |
| **기대 (플랜 샘플 표기)** | `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` |
| **PRD 공식 코드** | `ERR_INVALID_SHAPE` — `Input must be a 4x4 integer matrix.` |
| **Domain 호출** | **No** (BR-05, EP-01) |

### 4.2 선택 이유

1. FR-01 Acceptance Criteria·불변식 I-1 의존 순서상, `grid=None`은 빈칸·범위·중복 검사보다 **가장 선행**되는 형태/존재 검증이다.
2. 동일 시나리오에서 Boundary 오류 반환과 Domain 진입점 미호출(**RED-BND-006** / BR-05)을 한 플랜에 묶어 **Boundary 계약 + 호출 격리**를 동시에 검증할 수 있다.

## 5) 개발 To-Do List (추적 보드) 요약

### 5.1 Epic · User Stories

| ID | 요약 |
|----|------|
| Epic-001 | 불변식 기반 사고 훈련 시스템 — Concept→Test 추적 |
| US-001 | Boundary 입력 검증 (FR-01) |
| US-002 | BlankFinder row-major (FR-02) |
| US-003 | MissingNumberFinder 오름차순 (FR-03) |
| US-004 | MagicSquareValidator 행/열/대각 34 (FR-04) |
| US-005 | Solver small-first/reverse + int[6] (FR-05) |
| US-006 | ECB·품질 게이트 (NFR, Report/3) |

### 5.2 TDD 흐름 (보드 공통)

```text
Scenario → AC → RED Test ID → Test Skeleton → Run Test
  → Confirm Failure = RED → GREEN Task Candidate → REFACTOR Candidate
```

| 단계 | 정의 |
|------|------|
| **RED** | 테스트 실행 후 **의도된 실패 상태 확인** (ImportError·AssertionError) |
| **GREEN** | RED 1건 통과용 **최소 구현 후보** (실제 구현 아님, 계획만) |
| **REFACTOR** | GREEN 이후 구조 개선 **후보** (미수행) |

### 5.3 Track · Task 개수

| Track | TASK 범위 | RED ID 예 |
|-------|-----------|-----------|
| Boundary RED | TASK-001~009 | RED-BND-001~009 |
| Logic RED | TASK-010~019 | RED-DOM-001~010 |
| Integration RED | TASK-020~021 | RED-INT-001~002 |

### 5.4 필수 Scenario 커버리지 (§6 Tracking Board)

| Scenario ID | 요약 | RED Test ID |
|-------------|------|-------------|
| SC-BND-001 | None 입력 | RED-BND-001 |
| SC-BND-002 | 4×4 아님 | RED-BND-002 |
| SC-BND-003 | 빈칸 개수 오류 | RED-BND-003 |
| SC-BND-004 | 값 범위 오류 | RED-BND-004 |
| SC-BND-005 | 중복 숫자 | RED-BND-005 |
| SC-DOM-001 | row-major 빈칸 | RED-DOM-001 |
| SC-DOM-002 | 누락 숫자 오름차순 | RED-DOM-002 |
| SC-DOM-003~005 | 행/열/대각 합 34 | RED-DOM-003~005 |
| SC-DOM-006~008 | small-first / reverse / both fail | RED-DOM-007~009 |
| SC-BND-006~007 | int[6] 길이 / 1-index | RED-BND-008~009 |

### 5.5 권장 RED 착수 순서

1. Track A: RED-BND-001 → 005 → 006 (격리) → 007  
2. Track B: RED-DOM-001 → 002 → 003 → 004 → 005 → 015  
3. Control: RED-DOM-007 → 008 → 009  
4. 출력: RED-BND-008 → 009  
5. Integration: RED-INT-001 → 002  

## 6) README 시작 가이드 초안 요약

| 섹션 | 내용 |
|------|------|
| §1 Project Start Declaration | PRD 기반 TDD 준비, RED=실패 확인, 구현 전 가이드 |
| §2 PRD Summary | 목적·도메인·입출력·성공 기준 |
| §3 TDD Development Flow | 8단계 흐름 정의 |
| §4 Methodology | Dual-Track, Traceability, RED→GREEN→REFACTOR |
| §5 ECB | Entity / Control / Boundary 표 |
| §6 Tracking Board | 15+ Scenario 행 (Status `- [ ]`) |
| §7 RED Start Checklist | 11항 |
| §8 Quality Gates | 95%/85%, pytest, AAA, 금지 규칙 |
| §9 Reference Documents | PRD, Report 01~07, .mdc |
| §10 Current Status | 구현·테스트 전, 다음=Skeleton+RED |

> README 본문은 채팅 산출물이며 **루트 `README.md`에 아직 병합하지 않음**. 병합 시 기존 Report/01~07 타임라인과 통합 편집 권장.

## 7) OPEN 항목 (RED 착수 전)

| ID | 내용 | 출처 |
|----|------|------|
| OPEN-01 | `INVALID_SIZE` vs `ERR_INVALID_SHAPE` 명칭 통일 | 샘플 vs PRD §13 |
| OPEN-02 | TD-02 small-first 입력 행렬 확정 | PRD §16.4, Report/07 P0 |
| OPEN-03 | TD-07 no-solution 입력 행렬 확정 | PRD §16.4 |
| OPEN-04 | AC-FR02-01, AC-FR02-03, AC-FR03-03 Matrix 연결 | Report/07 |

## 8) 생성·수정 파일

| 경로 | 설명 |
|------|------|
| `Report/08MagicSquare-TDD-Start-ToDo-README-Report.md` | 본 보고서 |
| `Prompt/08cursor_magicsquare_tdd_start_todo_readme_transcript.md` | 세션 Transcript Export |
| `Report/README.md` | 문서 인덱스 갱신 |

## 9) 후속 권장

1. 에러 코드·메시지 OPEN-01 확정 후 Tracking Board 일괄 반영  
2. 루트 `README.md`에 §1~§10 시작 가이드 병합 (기존 타임라인 유지)  
3. `tests/boundary/test_magic_square_validator.py` Test Skeleton 작성 → **RED 실패 확인**  
4. PRD v0.2: TD-02/TD-07, Matrix AC 3건 보완  
5. `RED-BND-001` GREEN 최소 구현 (`BoundaryValidator` None 분기)

## 10) 결론

Magic Square 4×4 프로젝트는 **PRD·Scenario·AC·RED Test ID까지 추적 구조가 갖춰진 상태**이며,
**구현·마방진 테스트 코드는 미착수**이다.

다음 공식 단계는 **Test Skeleton 작성 → pytest 실행 → Confirm Failure = RED**이다.
