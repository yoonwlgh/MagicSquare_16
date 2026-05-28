# PRD — Magic Square 4x4 TDD Practice

| 항목 | 내용 |
|---|---|
| **문서 ID** | PRD-MS-4X4-001 |
| **버전** | 0.1.0-draft |
| **상태** | 구현 전 기준 문서 (Pre-Implementation) |
| **대상 저장 경로** | `docs/PRD_MagicSquare.md` |
| **작성 기준일** | 2026-05-29 |
| **근거 문서** | Report/1 (→ `01MagicSquare-Problem-Definition-Report.md`), Report/2 (→ `02MagicSquare-TDD-Design-Report.md`), Report/3 (→ `03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md`), Report/4 (→ `06MagicSquare-UserJourney-Story-Scenario-Report.md`), `.cursorrules`, `.cursor/rules/*.mdc` |

---

## 1. Executive Summary

Magic Square 4x4 TDD Practice는 **4×4 정수 격자에서 빈칸 2개를 채워 유효한 마방진을 만드는 Solver**를 구현하기 위한 프로젝트가 아니라, **불변식·입출력 계약·Boundary/Domain 분리·Dual-Track TDD·회귀 가능한 Traceability**를 훈련하기 위한 구현 전 기준 문서이다. 본 PRD는 사용자에게 `int[6]` 형식의 좌표·숫자 결과를 반환하되, 그 전에 Boundary에서 입력 계약을 검증하고, Domain에서 빈칸 탐색·누락 숫자 계산·마방진 판정·두 조합 시도를 수행한다.

**훈련하려는 핵심 역량**

| 역량 | PRD에서의 표현 |
|---|---|
| **불변식 사고** | BR-01~BR-14, I-1~I-10 계열 규칙을 독립 검증 가능한 Business Rule로 고정 |
| **입력/출력 계약** | §12 Input/Output Contract, §13 Error/Failure Policy |
| **Dual-Track TDD** | Track A(Boundary Contract)와 Track B(Domain Invariant)를 분리 RED→GREEN→REFACTOR |
| **설계 → 테스트 → 구현 → 리팩토링** | §15 Dual-Track TDD Strategy, §16 Test Plan, §21 Traceability Matrix |

---

## 2. Background

Report/1에 따르면, 4×4 마방진 과제의 **표면 목표**는 「행·열·대각선 합이 34인 격자를 만든다」이지만, **정확한 목표**는 「명시된 제약을 만족하는지 판정·해결하는 규칙을 정의하고, 그 규칙을 반복 가능하게 적용하며, 기준을 테스트로 고정·회귀할 수 있게 하는 것」이다.

본 프로젝트는 알고리즘 난이도·최적 생성·해 enumeration이 목적이 아니다. Report/1의 Why #2~#3에서 드러난 문제—**손계산 한 번으로 끝나는 답**, **검증 누락**, **규칙 혼동**, **책임 한 덩어리**—를 프로그램과 TDD로 해소한다. Report/4의 Epic은 이를 「불변식 기반 사고 훈련 시스템 구축」으로 정리한다.

**UI, DB, Web 없이 순수 로직 기반**으로 구현 가능하도록 PRD를 작성한다. 실행 환경은 콘솔 또는 pytest 실행 중심이다.

---

## 3. Problem Statement

### 3.1 정의

> **4×4 정수 격자(빈칸 2개)에 대해, Boundary 입력 계약을 검증하고, Domain 불변식(값 범위·중복·마방진 합·조합 시도 순서)을 만족하는 해를 찾아, 1-index 기준 `int[6]` 결과를 반환하는 규칙을 테스트 가능한 계약으로 고정한다.**

### 3.2 「마방진을 만든다」가 아닌 이유

| 표면 정의 (비채택) | 본 PRD 정의 (채택) |
|---|---|
| 34가 되는 격자 한 장을 만든다 | 입력/출력 계약과 불변식을 검증 가능하게 고정한다 |
| 성공 = 정답 출력 | 성공 = 계약·불변식·회귀 테스트 통과 |
| 구현 먼저 | RED 테스트로 요구사항 먼저 고정 |

### 3.3 입력/출력 계약이 핵심인 이유

Report/2와 Report/4에 따르면, 입력 형태·빈칸 정의·좌표 기준·출력 배열 길이·조합 시도 순서가 모호하면 **맞는데 틀리게 판정**되거나 **Boundary와 Domain 책임이 섞인다**. 본 PRD는 §12 계약과 §13 실패 정책으로 이 모호함을 닫는다.

---

## 4. Why Now / Why Chain

### 4.1 Why Chain 요약 (Report/1)

| 단계 | 질문 | 결론 |
|---|---|---|
| Why #1 | 왜 완성해야 하는가 | 제출·증명 목적이지만, 「완성」 기준이 모호하면 대리 지표(격자 한 장)만 맞추게 됨 |
| Why #2 | 왜 프로그램인가 | 반복 가능한 절차, 자동 검증, 규칙 분해, 오류 방지 |
| Why #3 | 왜 TDD인가 | 다중 불변식, 판정/생성 책임 혼동, 입출력 모호함을 **계약과 테스트**로 통제 |

### 4.2 Why Now

구현 착수 전에 PRD가 필요한 이유:

| 학습자 Pain Point | PRD가 닫는 것 |
|---|---|
| 구현을 먼저 시작함 | FR·BR·AC·Test Case Candidate를 구현 전에 고정 |
| 테스트 기준이 불명확함 | §16 Test Plan, §21 Traceability Matrix |
| Boundary와 Domain 책임이 섞임 | §17 Architecture, §15 Dual-Track |
| 리팩토링 후 계약이 깨짐 | REFACTOR 단계 계약 보존 규칙, 회귀 시나리오 |

---

## 5. Target Users

| 사용자 | 목적 | 사용 환경 |
|---|---|---|
| **TDD 학습자** | RED-GREEN-REFACTOR, Dual-Track 훈련 | pytest, 콘솔 실행 |
| **코드 리뷰어** | 계약·불변식·레이어 분리 검증 | PR, 테스트 결과, Traceability Matrix |
| **Clean Architecture + ECB 학습 개발자** | Boundary→Control→Domain 의존 방향 훈련 | 로컬 개발 환경 |

**범위 밖 사용자 환경:** 실제 UI 화면, DB, Web/API, 외부 서비스 연동.

---

## 6. Vision & Epic Goal

### 6.1 Vision

**Concept → Invariant → Contract → Test → Component** 추적성을 갖춘, 불변식 중심 TDD 훈련 시스템.

### 6.2 Epic Goal (Report/4)

**Epic:** `불변식 기반 사고 훈련 시스템 구축`

| Epic 하위 목표 | 검증 가능 기준 |
|---|---|
| 불변식 중심 설계 | §21 Traceability Matrix의 모든 Concept가 BR·FR·Test에 연결됨 |
| Dual-Track UI + Logic TDD | Track A/B RED가 분리되어 존재함 |
| 입력/출력 계약 명확화 | §12 계약 표의 모든 Rule이 AC 또는 Test Case Candidate와 연결됨 |
| 설계→테스트→구현→리팩토링 정착 | §15.3 Parallel Progression Rules 준수 |
| 회귀 보호 | §16 Normal/Exception/Boundary 시나리오 전부 회귀 대상 |

### 6.3 Epic Success Criteria (Report/4 + 본 PRD NFR)

| ID | 기준 | 측정 방법 |
|---|---|---|
| SC-01 | Domain Logic test coverage ≥ 95% | pytest-cov, Domain 레이어 대상 |
| SC-02 | Boundary Validation test coverage ≥ 85% | pytest-cov, Boundary 레이어 대상 |
| SC-03 | Boundary 입력 검증 계약 테스트 100% 통과 | §16 Exception Scenarios 전부 GREEN |
| SC-04 | 명명된 상수 사용, 설명 없는 magic number 0건 | 코드 리뷰 + 정적 검사 |
| SC-05 | 정답 하드코딩 0건 | 특정 입력→고정 `int[6]` 직접 반환 금지 검증 |
| SC-06 | 주요 Invariant별 테스트 추적 가능 | §21 Matrix |
| SC-07 | REFACTOR 후 외부 입출력 계약 유지 | 계약 테스트 회귀 GREEN |

---

## 7. Persona

### 7.1 Persona A — TDD 학습 개발자 「민준」

| 항목 | 내용 |
|---|---|
| **목표** | RED부터 작성하고, Boundary/Domain을 섞지 않음 |
| **Pain Point** | 「일단 돌아가게」 구현 후 테스트가 형식적임 |
| **성공 상태** | FR별 AC를 테스트로 표현하고, Traceability Matrix로 연결함 |

### 7.2 Persona B — 아키텍처 학습자 「서연」

| 항목 | 내용 |
|---|---|
| **목표** | ECB/Clean Architecture 레이어 분리 이해 |
| **Pain Point** | Boundary에서 Domain 규칙을 직접 호출함 |
| **성공 상태** | Boundary→Control→Domain 의존 방향을 코드와 테스트 모두에서 유지함 |

### 7.3 Persona C — 설계·계약 중심 학습자 「지훈」

| 항목 | 내용 |
|---|---|
| **목표** | 알고리즘 정답보다 계약·불변식·리팩토링 훈련 |
| **Pain Point** | small-first/reverse, row-major 정의 누락으로 테스트가 엇갈림 |
| **성공 상태** | §12·§13 계약과 §16 Test Data가 일치함 |

---

## 8. User Journey Summary

| Stage | Pain Point | Learning Outcome | 관련 FR |
|---|---|---|---|
| **1. 문제 인식** | 「정답 구현」만 목표로 삼음 | 판정·Solver를 **계약 문제**로 재정의 | FR-04, FR-05 |
| **2. 계약 정의** | 입력/출력/실패 기준 불명 | §12·§13 계약을 구현 전에 고정 | FR-01, §12 |
| **3. 도메인 분리** | Boundary에 Domain 규칙 혼입 | BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver 책임 분리 | FR-02~FR-05 |
| **4. Dual-Track TDD** | UI/Logic RED를 한꺼번에 처리 | Track A/B 분리 RED→GREEN→REFACTOR | §15 |
| **5. 회귀 보호** | 리팩토링 후 계약 붕괴 | Normal/Exception/Boundary 시나리오 회귀 | §16 |

---

## 9. Scope

### 9.1 In-Scope

| ID | 범위 |
|---|---|
| IS-01 | 빈칸 좌표 탐색 (row-major, 정확히 2개) |
| IS-02 | 누락 숫자 2개 탐색 (0 제외, 1~16, 오름차순) |
| IS-03 | 마방진 판정 (행/열/주대각/부대각 합 = 34) |
| IS-04 | small-first → reverse 두 조합 Solver |
| IS-05 | Boundary 입력 검증 |
| IS-06 | 출력 `int[6]` 계약 검증 |
| IS-07 | RED-GREEN-REFACTOR에 맞는 테스트 가능 요구사항 |
| IS-08 | Control 레이어를 통한 Boundary↔Domain 조율 |

### 9.2 Out-of-Scope

| ID | 제외 항목 |
|---|---|
| OS-01 | UI 화면 개발 |
| OS-02 | DB 저장/검색 |
| OS-03 | Web/API 서버 개발 |
| OS-04 | N×N 일반화 |
| OS-05 | 완전한 마방진 생성 알고리즘 (빈칸 2개 Solver 범위 외 생성) |
| OS-06 | 사용자 인증/권한 |
| OS-07 | 네트워크 오류 처리 |
| OS-08 | QR 스캔 |
| OS-09 | 외부 서비스 연동 |

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)

| 항목 | 내용 |
|---|---|
| **Description** | Boundary는 Domain Solver 파이프라인 호출 전에 입력 행렬의 형태·빈칸 개수·값 범위·중복 규칙을 검증한다. |
| **Layer** | Boundary |
| **Input** | `int[][]` (4×4 기대) |
| **Processing Rules** | BR-01, BR-02, BR-03, BR-04, BR-05 위반 시 즉시 실패 응답. Domain Solver 미호출. |
| **Output** | 성공: Control에 검증 통과 입력 전달. 실패: §13 Error Response. |
| **Acceptance Criteria** | AC-FR01-01: 3×4 입력 시 `ERR_INVALID_SHAPE`, Domain 미호출. AC-FR01-02: 빈칸 1개/3개 시 `ERR_INVALID_BLANK_COUNT`, Domain 미호출. AC-FR01-03: 17 포함 시 `ERR_OUT_OF_RANGE`, Domain 미호출. AC-FR01-04: 0 제외 중복 시 `ERR_DUPLICATE_VALUE`, Domain 미호출. AC-FR01-05: 유효 입력 시 Boundary 검증 테스트 GREEN 후 Control 호출 가능. |
| **Error / Exception Policy** | §13 ERR_INVALID_SHAPE, ERR_INVALID_BLANK_COUNT, ERR_OUT_OF_RANGE, ERR_DUPLICATE_VALUE |
| **Related Business Rules** | BR-01~BR-05 |
| **Related Test Direction** | Track A: RED-BND-VAL-001~003 (Report/4) |
| **Component Candidate** | BoundaryValidator |

---

### FR-02 Blank Coordinate Discovery (Domain)

| 항목 | 내용 |
|---|---|
| **Description** | Domain은 입력 행렬에서 `0`인 빈칸 좌표 2개를 row-major 순서로 반환한다. |
| **Layer** | Domain |
| **Input** | Boundary 검증을 통과한 `int[][]` |
| **Processing Rules** | BR-02, BR-06. 첫 번째 빈칸 = row-major 최초 `0`. 두 번째 빈칸 = row-major 두 번째 `0`. |
| **Output** | 내부 구조: `[(r1,c1), (r2,c2)]` (0-index 내부 표현). 외부 출력 전 Formatter에서 1-index 변환. |
| **Acceptance Criteria** | AC-FR02-01: 빈칸 2개 좌표를 정확히 반환. AC-FR02-02: row-major 순서 보장. AC-FR02-03: 0-index 내부 좌표와 1-index 외부 좌표 변환 규칙 일치. |
| **Error / Exception Policy** | FR-01 통과 입력만 수신. 빈칸 개수 오류는 FR-01 책임. |
| **Related Business Rules** | BR-02, BR-06 |
| **Related Test Direction** | Track B: BlankFinder 단위 RED |
| **Component Candidate** | BlankFinder |

---

### FR-03 Missing Number Discovery (Domain)

| 항목 | 내용 |
|---|---|
| **Description** | Domain은 `0`을 제외한 입력 값 집합과 `{1..16}`의 차집합에서 누락 숫자 2개를 계산한다. |
| **Layer** | Domain |
| **Input** | Boundary 검증 통과 `int[][]` |
| **Processing Rules** | BR-07, BR-08. 반환 순서는 오름차순 `[small, large]`. |
| **Output** | `[missingSmall, missingLarge]` |
| **Acceptance Criteria** | AC-FR03-01: 누락 숫자 정확히 2개. AC-FR03-02: 오름차순 반환. AC-FR03-03: `0`은 누락 후보에서 제외. |
| **Error / Exception Policy** | FR-01 통과 입력만 수신. |
| **Related Business Rules** | BR-07, BR-08 |
| **Related Test Direction** | Track B: MissingNumberFinder RED |
| **Component Candidate** | MissingNumberFinder |

---

### FR-04 Magic Square Validation (Domain)

| 항목 | 내용 |
|---|---|
| **Description** | Domain은 완성된 4×4 격자가 마방진 불변식을 만족하는지 판정한다. |
| **Layer** | Domain |
| **Input** | 빈칸이 채워진 4×4 `int[][]` |
| **Processing Rules** | BR-03, BR-04, BR-09, BR-10, BR-11. 모든 행·열·주대각·부대각 합 = 34. 0 제외 값 중복 없음. 값 범위 1~16. |
| **Output** | `isValid: boolean` (내부). 유효할 때만 Solver 다음 단계 진행. |
| **Acceptance Criteria** | AC-FR04-01: 모든 라인 합 34일 때만 `true`. AC-FR04-02: 하나라도 34가 아니면 `false`. AC-FR04-03: 합은 34이나 중복 있으면 `false`. |
| **Error / Exception Policy** | 판정 실패는 Solver 조합 시도 실패로 이어짐. 별도 Boundary Error Code 없음. |
| **Related Business Rules** | BR-03, BR-04, BR-09, BR-10, BR-11 |
| **Related Test Direction** | Track B: MagicSquareValidator RED |
| **Component Candidate** | MagicSquareValidator |

---

### FR-05 Two-Combination Solver and Result Formatting (Control + Domain + Boundary)

| 항목 | 내용 |
|---|---|
| **Description** | Control은 Domain Solver로 두 조합을 순서대로 시도하고, 성공 시 `int[6]`을 Boundary가 계약에 맞게 반환한다. |
| **Layer** | Control (조율), Domain (Solver), Boundary (출력 포맷 검증) |
| **Input** | FR-01 통과 `int[][]` |
| **Processing Rules** | **Attempt 1 (small-first):** `missingSmall→blank1`, `missingLarge→blank2`. 유효하면 `[r1,c1,n1,r2,c2,n2]` 반환 (1-index, n1=small, n2=large). **Attempt 2 (reverse):** Attempt 1 실패 시 `missingLarge→blank1`, `missingSmall→blank2`. 유효하면 동일 좌표에 `[r1,c1,n2,r2,c2,n1]` 반환. **Both fail:** §13 `ERR_SOLVER_NO_SOLUTION`. |
| **Output** | 성공: `int[6]`. 실패: Error Response (§13). |
| **Acceptance Criteria** | AC-FR05-01: small-first 성공 시 small→blank1, large→blank2 순서 반환. AC-FR05-02: small-first 실패·reverse 성공 시 `[3,3,6,4,4,1]` (Report/4 SC-DOM-SOL-001). AC-FR05-03: 두 조합 모두 실패 시 `ERR_SOLVER_NO_SOLUTION`, `int[6]` 미반환. AC-FR05-04: 반환 배열 길이 = 6. AC-FR05-05: 좌표 1-index. |
| **Error / Exception Policy** | §13 ERR_SOLVER_NO_SOLUTION |
| **Related Business Rules** | BR-06~BR-14 |
| **Related Test Direction** | Track B: RED-DOM-SOL-001; Track A: 출력 형식 RED |
| **Component Candidate** | Solver, ResultFormatter |

---

## 11. Business Rules / Domain Rules

| ID | Rule (항상 참) | 검증 방법 |
|---|---|---|
| **BR-01** | 입력은 정확히 4행 4열 `int[][]`이어야 한다. | 3×4, 4×3, jagged array → 실패 |
| **BR-02** | `0`인 빈칸은 정확히 2개이어야 한다. | 빈칸 0/1/3+개 → `ERR_INVALID_BLANK_COUNT` |
| **BR-03** | 각 칸 값은 `0` 또는 `1~16` 정수여야 한다. | 17, 음수, null → `ERR_OUT_OF_RANGE` |
| **BR-04** | `0`을 제외한 숫자는 중복될 수 없다. | 동일 값 2회 이상 → `ERR_DUPLICATE_VALUE` |
| **BR-05** | Boundary 입력 검증 실패 시 Domain Solver 파이프라인은 호출되지 않는다. | Boundary 테스트에서 Domain mock/spy 미호출 검증 |
| **BR-06** | 첫 번째 빈칸은 row-major 스캔 최초 `0` 좌표이다. | 좌표 순서 테스트 |
| **BR-07** | 누락 숫자는 `{1..16} \ {입력의 0 제외 값}`에서 정확히 2개이다. | 집합 차집합 테스트 |
| **BR-08** | 누락 숫자 반환 순서는 오름차순 `[small, large]`이다. | `[small, large]` where small < large |
| **BR-09** | 4×4 마방진 마법 상수 M = 34이다. | 명명 상수 `MAGIC_CONSTANT = 34` |
| **BR-10** | 각 행·열·주대각·부대각선 합은 34이어야 한다. | 라인별 합 테스트 |
| **BR-11** | 마방진 판정은 BR-10과 BR-04를 동시에 만족할 때만 유효이다. | 합 34 + 중복 케이스 무효 |
| **BR-12** | Solver Attempt 1: small→blank1, large→blank2. | small-first 성공 시나리오 |
| **BR-13** | Solver Attempt 2: Attempt 1 실패 시 large→blank1, small→blank2. | reverse 성공 시나리오 |
| **BR-14** | 외부 출력 좌표는 1-index, 형식 `[r1,c1,n1,r2,c2,n2]`, 배열 길이 6. | Boundary 출력 계약 테스트 |

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Error Code / Failure Policy |
|---|---|---|---|---|---|
| `grid` | `int[][]` | 4 rows × 4 cols | 4×4 matrix | 3×4 matrix | `ERR_INVALID_SHAPE` |
| `grid[r][c]` | `int` | `0` or `1..16` | `5`, `0` | `17`, `-1` | `ERR_OUT_OF_RANGE` |
| blank cells | count | exactly `2` | two `0` cells | one `0` | `ERR_INVALID_BLANK_COUNT` |
| non-zero values | set | all unique | `{1,2,4,...,16}` minus blanks | duplicate `7` | `ERR_DUPLICATE_VALUE` |
| first blank | coordinate | row-major first `0` | `(2,2)` 0-index | undefined order | N/A (internal) |

### 12.2 Output Contract (Success)

| Field / Item | Type | Rule | Valid Example | Invalid Example | Failure Policy |
|---|---|---|---|---|---|
| result | `int[6]` | length = 6 | `[3,3,6,4,4,1]` | length 5 or 7 | Boundary format validation fail |
| r1, c1, r2, c2 | `int` | 1-index, range 1..4 | `3,3,4,4` | `0,5` | format validation fail |
| n1, n2 | `int` | missing numbers per attempt rule | `6,1` (reverse case) | out of 1..16 | domain logic fail |
| order | rule | Attempt 1: n1=small, n2=large; Attempt 2 success: n1=large, n2=small | `[3,3,6,4,4,1]` | swapped without rule | AC-FR05-02 fail |

### 12.3 Output Contract (Failure)

| Condition | Error Code | Response Shape | Domain Called? |
|---|---|---|---|
| Not 4×4 | `ERR_INVALID_SHAPE` | `{ code, message, layer: "Boundary" }` | No |
| Blank count ≠ 2 | `ERR_INVALID_BLANK_COUNT` | same | No |
| Value out of range | `ERR_OUT_OF_RANGE` | same | No |
| Duplicate non-zero | `ERR_DUPLICATE_VALUE` | same | No |
| Both combinations invalid | `ERR_SOLVER_NO_SOLUTION` | `{ code, message, layer: "Control" }` | Yes (Solver exhausted) |

---

## 13. Error / Failure Policy

### 13.1 정책 원칙

| ID | Policy |
|---|---|
| **EP-01** | 입력 검증 실패 시 Domain Solver 파이프라인(BlankFinder, MissingNumberFinder, Solver)은 **호출되지 않는다**. |
| **EP-02** | Solver 두 조합 모두 실패 시 **`int[6]`을 반환하지 않는다**. |
| **EP-03** | EP-02의 실패는 Error Code **`ERR_SOLVER_NO_SOLUTION`** 으로 반환한다. (예외 throw가 아닌 **구조화된 Error Response** — §22 Decision Needed 참고) |
| **EP-04** | Domain 로직은 입력 행렬을 **변경하지 않는다** (immutable input policy). |

### 13.2 Error Catalog

| Error Code | Message (기본) | Layer | Domain Resolver 호출 | Related AC |
|---|---|---|---|---|
| `ERR_INVALID_SHAPE` | Input must be a 4x4 integer matrix. | Boundary | No | AC-FR01-01 |
| `ERR_INVALID_BLANK_COUNT` | Input must contain exactly 2 blank cells (0). | Boundary | No | AC-FR01-02 |
| `ERR_OUT_OF_RANGE` | Cell values must be 0 or 1..16. | Boundary | No | AC-FR01-03 |
| `ERR_DUPLICATE_VALUE` | Non-zero values must be unique. | Boundary | No | AC-FR01-04 |
| `ERR_SOLVER_NO_SOLUTION` | No valid magic square combination found. | Control | Yes (both attempts failed) | AC-FR05-03 |

---

## 14. Non-Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| **NFR-01** | Domain Logic test coverage ≥ 95% | pytest-cov report |
| **NFR-02** | Boundary Validation test coverage ≥ 85% | pytest-cov report |
| **NFR-03** | Deterministic: 동일 입력 → 동일 출력 또는 동일 Error Code | 동일 입력 2회 실행 비교 테스트 |
| **NFR-04** | No side effects: Domain/Control은 입력 `int[][]` 원본을 변경하지 않음 | 입력 스냅샷 before/after 비교 |
| **NFR-05** | Performance: 4×4 단일 실행 ≤ 50ms (로컬 개발 환경) | 벤치마크 테스트 1회 median |
| **NFR-06** | Boundary와 Domain 책임 분리 | 아키텍처 리뷰 + 의존성 방향 테스트 |
| **NFR-07** | 정답 하드코딩 금지: 특정 입력에 대한 고정 `int[6]` 직접 반환 금지 | 코드 리뷰 |
| **NFR-08** | 설명 없는 magic number 금지; `MAGIC_CONSTANT=34`, `GRID_SIZE=4` 등 명명 상수 사용 | 정적 검사 + 리뷰 |
| **NFR-09** | pytest, AAA 패턴, `test_` 접두사 | 테스트 코드 리뷰 |
| **NFR-10** | RED 확인 전 production 구현 금지 | 프로세스 리뷰 |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD

| ID | Test Target | Example RED ID |
|---|---|---|
| TA-01 | 4×4 형태 검증 | RED-BND-VAL-001 |
| TA-02 | 빈칸 2개 검증 | RED-BND-VAL-001 |
| TA-03 | 0 제외 중복 검증 | RED-BND-VAL-002 |
| TA-04 | 값 범위 검증 | RED-BND-VAL-003 |
| TA-05 | 출력 `int[6]` 길이·1-index 검증 | RED-BND-FMT-001 |
| TA-06 | 입력 검증 실패 시 Domain 미호출 | RED-BND-ISO-001 |
| TA-07 | `ERR_*` Error Response 형식 | RED-BND-ERR-001 |

### 15.2 Track B — Domain / Logic Invariant TDD

| ID | Test Target | Example RED ID |
|---|---|---|
| TB-01 | BlankFinder row-major 2좌표 | RED-DOM-BLK-001 |
| TB-02 | MissingNumberFinder 오름차순 2개 | RED-DOM-MIS-001 |
| TB-03 | MagicSquareValidator 합 34 | RED-DOM-VAL-001 |
| TB-04 | small-first 성공 | RED-DOM-SOL-002 |
| TB-05 | small-first 실패 → reverse 성공 | RED-DOM-SOL-001 |
| TB-06 | 두 조합 모두 실패 | RED-DOM-SOL-003 |
| TB-07 | 입력 행렬 불변 | RED-DOM-IMM-001 |

### 15.3 Parallel Progression Rules

| ID | Rule |
|---|---|
| **DT-01** | Track A RED와 Track B RED는 **분리된 테스트**로 작성한다. |
| **DT-02** | Track A GREEN과 Track B GREEN은 **각각 최소 구현**으로만 통과시킨다. |
| **DT-03** | 구조 개선은 **REFACTOR 단계에서만** 수행한다. |
| **DT-04** | 모든 Domain 구현 후 Boundary를 붙이는 **Waterfall 순서를 금지**한다. Track A/B를 병렬 또는 짧은 주기로 교차 진행한다. |
| **DT-05** | 테스트 skip, assertion 삭제, 기대값 완화로 통과시키는 것을 **금지**한다. |
| **DT-06** | REFACTOR 후 Track A/B 계약 테스트가 **모두 GREEN**이어야 한다. |

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | Scenario | Given | When | Then |
|---|---|---|---|---|
| **NS-01** | small-first 성공 | 유효 4×4, Attempt 1이 마방진 | solve | `int[6]`, n1=small, n2=large |
| **NS-02** | reverse 성공 | 유효 4×4, Attempt 1 실패·Attempt 2 성공 | solve | `[3,3,6,4,4,1]` (Report/4 SC-DOM-SOL-001) |

### 16.2 Exception Scenarios

| ID | Scenario | Expected Error | Domain Called |
|---|---|---|---|
| **ES-01** | 4×4 아님 | `ERR_INVALID_SHAPE` | No |
| **ES-02** | 빈칸 ≠ 2 | `ERR_INVALID_BLANK_COUNT` | No |
| **ES-03** | 값 범위 위반 | `ERR_OUT_OF_RANGE` | No |
| **ES-04** | 0 제외 중복 | `ERR_DUPLICATE_VALUE` | No |
| **ES-05** | 두 조합 모두 실패 | `ERR_SOLVER_NO_SOLUTION` | Yes |

### 16.3 Boundary Scenarios

| ID | Scenario | Expected |
|---|---|---|
| **BS-01** | 최소값 1 포함 | valid if other rules pass |
| **BS-02** | 최대값 16 포함 | valid if other rules pass |
| **BS-03** | `0`은 빈칸만 | non-blank cell with 0 → invalid (blank count rule) |
| **BS-04** | 출력 좌표 1-index | r,c ∈ {1,2,3,4} |
| **BS-05** | 반환 배열 길이 6 | `len(result)==6` |

### 16.4 Representative Test Data

| ID | Purpose | Notes | Expected |
|---|---|---|---|
| **TD-01** | reverse 성공 | Report/4 SC-DOM-SOL-001 입력 행렬 | `[3,3,6,4,4,1]` |
| **TD-02** | small-first 성공 | FR-05 Attempt 1만 성공하는 4×4 | `int[6]`, n1=small, n2=large |
| **TD-03** | invalid size | 3×4 matrix | `ERR_INVALID_SHAPE` |
| **TD-04** | invalid blank count | 1 or 3 zeros | `ERR_INVALID_BLANK_COUNT` |
| **TD-05** | duplicate value | two `7`s (non-zero) | `ERR_DUPLICATE_VALUE` |
| **TD-06** | invalid range | cell value 17 | `ERR_OUT_OF_RANGE` |
| **TD-07** | no solution | both combinations fail | `ERR_SOLVER_NO_SOLUTION` |

> **Note:** TD-02, TD-07의 구체 행렬 값은 구현 Phase RED 작성 시 확정한다. PRD는 **기대 결과 형태와 Error Code**만 고정한다.

---

## 17. Architecture Overview (High-Level)

### 17.1 Layer Responsibilities

| Layer | Responsibility | 금지 |
|---|---|---|
| **Boundary** | 입력 파싱·검증, Error Response, 출력 포맷 검증 | Domain 규칙 직접 구현, Entity 직접 접근 |
| **Control** | Use-case 조율, Solver Attempt 1→2 순서, 성공/실패 분기 | UI/DB/Web 의존, Domain 불변식 직접 재구현 |
| **Domain (Entity)** | BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver 순수 로직 | Boundary/Control/UI/DB/Web/파일시스템 의존 |

### 17.2 Dependency Direction

```text
Boundary → Control → Domain
```

| Rule | Statement |
|---|---|
| **AD-01** | Boundary MAY call Control. |
| **AD-02** | Control MAY call Domain. |
| **AD-03** | Domain MUST NOT depend on Boundary or Control. |
| **AD-04** | Boundary MUST NOT call Domain directly. |
| **AD-05** | Control MUST NOT depend on Boundary. |

### 17.3 Clean Architecture ↔ ECB Mapping

| Clean Architecture (개념) | ECB (본 프로젝트) |
|---|---|
| Interface Adapters | Boundary |
| Use Cases | Control |
| Entities / Domain Rules | Domain (Entity) |

---

## 18. Component Candidates

| Component | Layer | Responsibility | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| **BoundaryValidator** | Boundary | FR-01 입력 검증 | `int[][]` | pass / Error | FR-01 | RED-BND-VAL-* |
| **BlankFinder** | Domain | FR-02 빈칸 좌표 | validated grid | 2 coords (0-index) | FR-02 | RED-DOM-BLK-001 |
| **MissingNumberFinder** | Domain | FR-03 누락 숫자 | validated grid | `[small, large]` | FR-03 | RED-DOM-MIS-001 |
| **MagicSquareValidator** | Domain | FR-04 마방진 판정 | filled grid | boolean | FR-04 | RED-DOM-VAL-001 |
| **Solver** | Domain | FR-05 조합 시도 | grid + blanks + missing | filled grid or fail | FR-05 | RED-DOM-SOL-* |
| **ResultFormatter** | Boundary | FR-05 출력 변환 | internal result | `int[6]` 1-index | FR-05 | RED-BND-FMT-001 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Mitigation / Decision |
|---|---|---|
| 1-index vs 0-index 혼동 | 잘못된 좌표 반환 | BR-14, AC-FR02-03, BS-04; 내부 0-index / 외부 1-index 명시 |
| row-major 첫 빈칸 정의 누락 | Attempt 순서 오류 | BR-06, TB-01 |
| small-first vs reverse 테스트 데이터 혼동 | 잘못된 GREEN | TD-01/TD-02 분리, AC-FR05-01/02 |
| 입력 행렬 변경 | Side effect, NFR-04 위반 | EP-04, RED-DOM-IMM-001 |
| 두 조합 실패 정책 누락 | `int[6]` 오반환 | EP-02, EP-03, ERR_SOLVER_NO_SOLUTION |
| 34 상수 하드코딩 | 유지보수·리뷰 실패 | NFR-08, `MAGIC_CONSTANT` |
| Boundary/Domain 책임 혼합 | 아키텍처 붕괴 | AD-04, BR-05, DT-04 |
| Report/2 완성 격자 판정 vs 본 PRD Solver | 문서 충돌 | §22: 본 PRD 고정 계약 우선, Report/2는 판정 로직 재사용 참고 |

---

## 20. Engineering Principles

Report/3 및 Cursor Rules 요약:

| Principle | Requirement |
|---|---|
| **Python** | 3.10+ |
| **Style** | PEP8, line length 88 |
| **Typing** | 모든 public 함수/메서드 type hints 필수 |
| **Docstring** | Google style, public API 필수 |
| **Test framework** | pytest |
| **Test pattern** | AAA (Arrange-Act-Assert) |
| **Coverage** | Domain ≥95%, Boundary ≥85% (본 PRD NFR); 전체 minimum 80% (Cursor Rules) |
| **Architecture** | ECB: boundary / control / entity |
| **TDD** | Red → Green → Refactor 엄수 |
| **Prohibited** | `print()` 디버깅, bare `except:`, unexplained magic number, RED 없는 구현, 테스트 약화 |
| **Dependency** | boundary → control → entity |
| **Tests layout** | `tests/` mirrors layer structure |

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-01 | ES-01, RED-BND-VAL-001 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-FR01-02 | ES-02, RED-BND-VAL-001 | BoundaryValidator |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-03 | ES-03, RED-BND-VAL-003 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-04 | ES-04, RED-BND-VAL-002 | BoundaryValidator |
| Boundary 실패 시 Domain 미호출 | BR-05 | FR-01 | AC-FR01-05 | RED-BND-ISO-001 | BoundaryValidator |
| row-major 첫 번째 빈칸 | BR-06 | FR-02 | AC-FR02-02 | TB-01, RED-DOM-BLK-001 | BlankFinder |
| 누락 숫자 2개 | BR-07 | FR-03 | AC-FR03-01 | TB-02, RED-DOM-MIS-001 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-08 | FR-03 | AC-FR03-02 | TB-02 | MissingNumberFinder |
| 마방진 상수 34 | BR-09 | FR-04 | AC-FR04-01 | TB-03, RED-DOM-VAL-001 | MagicSquareValidator |
| 행/열/대각선 합 | BR-10, BR-11 | FR-04 | AC-FR04-01~03 | TB-03 | MagicSquareValidator |
| small-first 시도 | BR-12 | FR-05 | AC-FR05-01 | NS-01, TB-04 | Solver |
| reverse 시도 | BR-13 | FR-05 | AC-FR05-02 | NS-02, TB-05, RED-DOM-SOL-001 | Solver |
| 두 조합 실패 | EP-02, EP-03 | FR-05 | AC-FR05-03 | ES-05, TB-06, RED-DOM-SOL-003 | Solver, Control |
| int[6] 반환 | BR-14 | FR-05 | AC-FR05-04 | BS-05, TA-05 | ResultFormatter |
| 1-index 좌표 | BR-14 | FR-05 | AC-FR05-05 | BS-04, TA-05 | ResultFormatter |
| 입력 불변 | EP-04, NFR-04 | FR-02~05 | NFR-04 | TB-07, RED-DOM-IMM-001 | All Domain |
| Deterministic | NFR-03 | FR-05 | NFR-03 | NS-01/02 재실행 | Control |

---

## 22. Open Questions / Decision Needed

| ID | Issue | Related Source | Options | PRD Current Stance |
|---|---|---|---|---|
| **DN-01** | Solver 실패 시 Error Response vs Exception throw | User prompt vs Report/3 패턴 | (A) 구조화 Error Response (B) Domain Exception → Boundary mapping | **(A) 채택:** EP-03 `ERR_SOLVER_NO_SOLUTION` Error Response. 구현 시 Exception 내부 사용 여부는 Control 내부 선택 가능, **외부 계약은 Error Response 고정**. |
| **DN-02** | Report/2 완성 격자 판정(D-1~D-5) vs 본 PRD Solver 계약 | Report/2 vs User 고정 계약 | 병합 vs Solver PRD 우선 | **Solver PRD 우선.** MagicSquareValidator는 Report/2 판정 규칙을 Domain 내부 재사용 가능. |
| **DN-03** | Coverage: Domain 95%/Boundary 85% vs Cursor Rules 80% minimum | Report/4, `.mdc` | 계층별 상한 vs 전역 하한 | **둘 다 유효:** NFR-01/02 (층별) + Engineering Principles 80% minimum. 충돌 아님. |
| **DN-04** | TD-02, TD-07 구체 행렬 미확정 | 본 PRD | RED Phase에서 확정 | **Decision Needed:** RED 작성 시 TD-02/TD-07 행렬 고정 필요. |
| **DN-05** | Error Message 다국어/로컬라이제이션 | — | EN only vs KO | **EN default message** (§13.2). 로컬라이제이션 Out-of-Scope. |
| **DN-06** | Control 레이어 포함 범위 | Report/3 User slice | Control 필수 vs Boundary-Domain 직접 | **Control 필수** (§17, FR-05). |

---

## 23. Appendix

### 23.1 Reference Documents

| Logical Name | Repository Path |
|---|---|
| Report/1.ProblemDefinition | `Report/01MagicSquare-Problem-Definition-Report.md` |
| Report/2.CleanArchitecture_DualTrack_TDD_Design | `Report/02MagicSquare-TDD-Design-Report.md` |
| Report/3.DevelopmentEnvironment_CursorRules_ECB_UserEntity | `Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md` |
| Report/4.UserJourney_Epic_to_TechnicalScenario | `Report/06MagicSquare-UserJourney-Story-Scenario-Report.md` |
| Cursor Rules | `.cursorrules`, `.cursor/rules/*.mdc` |

### 23.2 Cursor Rules Summary

| File | Key Rules |
|---|---|
| `magicsquare-project.mdc` | 4×4, M=34, validation-first mindset |
| `magicsquare-ecb-architecture.mdc` | boundary/control/entity, dependency direction |
| `magicsquare-tdd-testing.mdc` | Dual-Track, pytest, AAA, 80% min, Red-Green-Refactor |
| `magicsquare-forbidden.mdc` | no print, no bare except, no magic number, no test weakening |
| `magicsquare-python-code-style.mdc` | PEP8, type hints, Google docstring |

### 23.3 Representative Gherkin Scenarios (Summary)

```gherkin
Feature: Boundary input validation
  Scenario: Reject invalid blank count
    Given a 4x4 grid that does not contain exactly 2 blank cells
    When the boundary validates the input
    Then the system returns ERR_INVALID_BLANK_COUNT
    And the domain solver pipeline is not invoked

Feature: Two-combination solver
  Scenario: Reverse combination succeeds after small-first fails
    Given a valid 4x4 grid with exactly 2 blank cells
    And small-first combination does not form a magic square
    And reverse combination forms a magic square
    When the solver runs
    Then the result is [3, 3, 6, 4, 4, 1]
```

### 23.4 Future RED Test ID Candidates

| Track | ID | Maps To |
|---|---|---|
| A | RED-BND-VAL-001 | ES-02 |
| A | RED-BND-VAL-002 | ES-04 |
| A | RED-BND-VAL-003 | ES-03 |
| A | RED-BND-ISO-001 | BR-05 |
| A | RED-BND-FMT-001 | BS-04, BS-05 |
| B | RED-DOM-SOL-001 | NS-02, TD-01 |
| B | RED-DOM-SOL-003 | ES-05, TD-07 |
| B | RED-DOM-IMM-001 | NFR-04 |

---

**문서 끝.**
