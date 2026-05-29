# MagicSquare_JH

4×4 **마방진(Magic Square)** 을 다루는 TDD 훈련 프로젝트입니다.

겉으로는 「행·열·대각선 합이 34가 되는 4×4 격자를 만든다」는 과제이지만, 이 저장소의 **진짜 목표**는 다음과 같습니다.

> **4×4 정수 격자가 명시된 제약을 만족하는지 판정하는 규칙을 정의하고, 그 판정을 반복 가능하게 적용하며, 기준을 테스트로 고정·회귀할 수 있게 하는 것**

유효한 격자 **하나를 산출**하는 Solver는, 위 판정 규칙이 확립된 뒤의 **2차 목표**로 둡니다.

---

## 현재 상태

| 단계 | 항목 | 상태 | 산출물 |
|------|------|------|--------|
| 1 | 문제 정의 (STEP 1~5) | ✅ 완료 | [Report/01](./Report/01MagicSquare-Problem-Definition-Report.md) |
| 2 | TDD 설계 (판정 1차, 생성 2차) | ✅ 완료 | [Report/02](./Report/02MagicSquare-TDD-Design-Report.md) |
| 3 | Cursor Rule + ECB User 수직 슬라이스 | ✅ 완료 | [Report/03](./Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md) |
| 4 | 규칙 분할 + Prompt 경로 통일 | ✅ 완료 | [Report/04](./Report/04MagicSquare-Rule-Expansion-and-Prompt-Export-Report.md) |
| 5 | TODO Web 기술 스택 검토 | ✅ 완료 | [Report/05](./Report/05TodoWeb-Stack-Recommendation-Report.md) |
| 6 | User Journey / Story / Scenario | ✅ 완료 | [Report/06](./Report/06MagicSquare-UserJourney-Story-Scenario-Report.md) |
| 7 | PRD 작성 + 7기준 검토 | ✅ 완료 | [Report/07](./Report/07MagicSquare-PRD-Development-and-Review-Report.md), [docs/PRD](./docs/PRD_MagicSquare.md) |
| 8 | 마방진 도메인 구현 (Solver/Validator) | 🟡 진행 중 | AC-FR-01-01 GREEN 완료; Dual-Track 스켈레톤 GREEN 대기 |

**코드 현황:** ECB `User` 슬라이스 **16 passed** + 마방진 Dual-Track **46건** + Golden Master **18건** (전체 GREEN).  
**전체 pytest:** `80 collected` — **80 passed**.

---

## 진행 타임라인

```text
STEP 1~5 문제 정의
    → TDD 설계 (불변식 I-1~I-10, P0 시나리오)
    → ECB + Cursor Rule + User 수직 슬라이스 (개발 환경 정착)
    → 규칙 .mdc 분할 + Prompt/Report 체계화
    → Epic → Journey → Story → Scenario 기획
    → PRD v0.1.0-draft + 7기준 검토
    → AC-FR-01-01 GREEN (25/25) 완료
    → [다음] Track A FR-01 후속(U-IN) → Track B Domain → U-OUT GREEN
```

---

## 문제 정의 요약

### 표면 정의 vs 정확한 정의

| 구분 | 내용 |
|------|------|
| **표면 (피해야 할 정의)** | 1~16을 넣어 행·열·대각 합이 모두 34인 배치를 **만든다** |
| **정확한 정의** | 제약(크기, 범위, 중복 없음, 선별 합 동일)을 **판정**하고, 그 규칙을 **고정·검증**한다 |

### 핵심 불변 조건 (Invariant)

4×4, 값 **1~16** 각 **한 번**, **마법 상수 34**:

- **I-1 ~ I-3:** 4×4 형태, 범위, 중복 없음
- **I-4 ~ I-7:** 각 행·열·주대각·부대각선 합 = 34
- **I-8 ~ I-10:** 전부 만족 시에만 유효, 동일 입력 → 동일 판정, 규칙 변경은 계약(테스트) 변경

상세: [Report/01 — 문제 정의 통합 보고서](./Report/01MagicSquare-Problem-Definition-Report.md)

---

## PRD 요약 (구현 전 기준)

| 항목 | 내용 |
|------|------|
| 문서 | [docs/PRD_MagicSquare.md](./docs/PRD_MagicSquare.md) |
| ID / 버전 | PRD-MS-4X4-001 / 0.1.0-draft |
| 핵심 FR | FR-01~FR-05 (Boundary 검증, Blank/Missing/Validator, Solver+Format) |
| Business Rules | BR-01~BR-14 |
| TDD 전략 | Dual-Track — Track A (Boundary Contract), Track B (Domain Invariant) |

### 고정 입출력 계약

**Input**

- 4×4 `int[][]`, `0` = 빈칸, 빈칸 정확히 2개
- 값: `0` 또는 `1~16`, 0 제외 중복 없음
- 첫 빈칸: row-major 최초 `0`

**Output**

- `int[6]`, 1-index, `[r1,c1,n1,r2,c2,n2]`
- Attempt 1: small→blank1, large→blank2
- Attempt 2: reverse 조합
- Both fail: `ERR_SOLVER_NO_SOLUTION`

PRD 7기준 검토 결과(부분 충족 항목·개선안): [Report/07 §5](./Report/07MagicSquare-PRD-Development-and-Review-Report.md)

---

## 아키텍처

### ECB 레이어

| 레이어 | 책임 | 예시 |
|--------|------|------|
| `boundary/` | 외부 I/O, 파싱·직렬화 | CLI, API adapter |
| `control/` | 유스케이스 조율 | Solver 파이프라인 순서 |
| `entity/` | 순수 도메인 규칙 | Validator, BlankFinder, Solver |

**의존 방향:** `boundary → control → entity` (역방향 금지)

### Dual-Track TDD

| Track | 대상 | RED 예시 |
|-------|------|----------|
| Track A | Boundary 입력/출력 계약 | 빈칸 개수 오류, 중복·범위 위반 거부 |
| Track B | Domain 불변식 | BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver |

---

## 저장소 구조

```text
MagicSquare_JH/
├── README.md                          # 이 파일
├── .cursorrules                       # 프로젝트 규칙 요약
├── .cursor/
│   ├── rules/                         # 주제별 Cursor Rule (.mdc)
│   └── agents/                        # code-reviewer, ux-design-advisor
├── boundary/                          # ECB — 외부 I/O
│   └── cli/user_cli_boundary.py
├── control/                           # ECB — 유스케이스 조율
│   └── user_control.py
├── entity/                            # ECB — 도메인 규칙
│   └── user.py
├── tests/                             # 레이어별 pytest (AAA)
│   ├── boundary/test_user_cli_boundary.py
│   ├── control/test_user_control.py
│   └── entity/test_user.py
├── docs/
│   └── PRD_MagicSquare.md             # 구현 전 PRD (23개 섹션)
├── Report/                            # 단계별 보고서
│   ├── README.md
│   ├── 01MagicSquare-Problem-Definition-Report.md
│   ├── 02MagicSquare-TDD-Design-Report.md
│   ├── 03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md
│   ├── 04MagicSquare-Rule-Expansion-and-Prompt-Export-Report.md
│   ├── 05TodoWeb-Stack-Recommendation-Report.md
│   ├── 06MagicSquare-UserJourney-Story-Scenario-Report.md
│   └── 07MagicSquare-PRD-Development-and-Review-Report.md
└── Prompt/                            # Cursor 대화·프롬프트 기록
    ├── 01cursor_4x4_magic_square_problem_definit.md
    ├── 02cursor_magicsquare_tdd_prompt_transcript.md
    ├── 03cursor_magicsquare_rule_ecb_transcript.md
    ├── 04cursor_magicsquare_rule_expansion_transcript.md
    ├── 05todo_web_stack_recommendation_transcript.md
    └── 06cursor_magicsquare_user_journey_story_scenario_transcript.md
```

---

## 개발 환경 및 테스트

### 요구 사항

- Python 3.10+
- pytest

### 테스트 실행

```bash
python -m pytest tests/ -v
```

Golden Master 회귀 테스트만 실행:

```bash
pytest -m golden_master -v
```

기준 파일 갱신: `python scripts/generate_golden_master.py` · 상세: [docs/README.md](./docs/README.md)

### HTML 테스트 리포트 (수동 갱신)

`pytest`만 실행하면 **HTML 리포트는 자동으로 갱신되지 않습니다.**  
마지막 생성본: `Report/pytest_report.html` (`.gitignore` 대상 — 로컬 파일만 갱신).

```powershell
.\.venv\Scripts\Activate.ps1
.\scripts\generate_test_report.ps1
```

또는:

```powershell
python -m pytest tests/ -v `
  --html=Report/pytest_report.html `
  --self-contained-html `
  --cov=boundary --cov=control --cov=entity `
  --cov-report=html:htmlcov `
  --cov-report=term-missing
```

브라우저에서 예전 결과가 보이면 **파일을 닫았다가 다시 열거나** 새로고침하세요.

### PyQt GUI (수동 확인)

4×4 격자 입력·검증·Solver 결과를 데스크톱에서 확인합니다.

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m boundary.screen
```

| 버튼 | 동작 |
|------|------|
| **Validate (FR-01)** | 형태·빈칸·범위·중복 검증 — 실패 시 `code: message` 표시 |
| **Solve (FR-05)** | 검증 통과 후 Solver — 성공 시 `Success: [r1,c1,n1,r2,c2,n2]` |
| **Reverse / Small-first sample** | TD-01·TD-02 샘플 격자 로드 |
| **Invalid blanks (×3)** | `ERR_INVALID_BLANK_COUNT` 확인용 |

ECB: UI는 `boundary/screen/` → `control/` → `entity/` 순으로 호출합니다.

| 구분 | passed | 비고 |
|------|--------|------|
| User ECB 슬라이스 | 16 | `test_user*.py` |
| AC-FR-01-01 | 25 | `test_ac_fr01_01_invalid_size.py` |
| Dual-Track U-IN/U-FLOW/U-OUT + D-* | 21 | Track A/B GREEN 완료 |
| Golden Master (GM-1~2) | 18 | `pytest -m golden_master -v` |
| **합계** | **80 / 80** | `python -m pytest tests/ -v` |

### Cursor Rule (.cursor/rules/)

| 파일 | 내용 |
|------|------|
| `magicsquare-project.mdc` | 프로젝트 범위, 마방진 도메인 목표 |
| `magicsquare-ecb-architecture.mdc` | ECB 레이어 책임·의존 방향 |
| `magicsquare-tdd-testing.mdc` | Dual-Track TDD, pytest, AAA, 80% 커버리지 |
| `magicsquare-python-code-style.mdc` | PEP8, 타입 힌트, Google docstring |
| `magicsquare-forbidden.mdc` | print 금지, bare except 금지, RED 선행 등 |

---

## User Story 요약 (Report/06)

| Story | 레이어 | 내용 |
|-------|--------|------|
| 1 | Boundary | 4×4, 빈칸 2개, 값 범위, 0 제외 중복 검증 — 실패 시 Domain 미호출 |
| 2 | Domain | `BlankFinder` — 0 탐지, 2개 좌표, row-major 순서 |
| 3 | Domain | `MissingNumberFinder` — 1~16 누락 2개, 오름차순 |
| 4 | Domain | `MagicSquareValidator` — 행/열/대각 합 34 동시 만족 |
| 5 | Control/Boundary | Solver — small-first 실패 시 reverse, `int[6]` 형식 보장 |

---

## 범위

### In scope

- 4×4 정수 격자 유효성 **판정** 규칙 (I-1 ~ I-10)
- 빈칸 2개 Solver 입출력 계약 (PRD §12)
- ECB 분리, Dual-Track TDD, pytest 회귀 보호
- 판정·Solver 규칙의 반복 가능성·테스트 고정

### Out of scope (현 단계)

- UI / Web / DB
- n×n 일반화, 모든 해 나열
- TODO Web 실제 구현 (Report/05는 기술 스택 **검토**만)

---

## 다음 단계

1. **Phase 0 (P0):** [그룹 A](#그룹-a--테스트-선행-회귀-안전망--p0) 테스트 GREEN → [그룹 B](#그룹-b--ecb-아키텍처-의존-방향--p0) Port/Adapter
2. **Phase 1 (P1):** [그룹 C-1](#c-1-control--boundary-핵심--p1) SRP 분리
3. **Phase 2~3 (P2~P3):** [그룹 C-2, D, E](#그룹-d--계약상수중복-정리--p2) 계약·UI·문서
4. 상세 체크리스트: [REFACTOR 계획](#refactor-계획) · [Report/15](./Report/15MagicSquare-REFACTOR-Plan-Report.md)

---

## REFACTOR 계획

> **전제:** `.cursorrules` REFACTOR phase — 외부 동작·계약·예외 의미 불변, 커버리지 80% 유지, GREEN 전체 통과 후 착수.  
> **범위:** `control/`, `boundary/` (루트 ECB)  
> **현재 baseline:** `80 passed` · `pytest -m golden_master` → 18 passed  
> **상세 보고서:** [Report/15 — REFACTOR 계획](./Report/15MagicSquare-REFACTOR-Plan-Report.md)  
> **표기:** `[ ]` 미완 · `[x]` 완료 · **P0→P3** = 우선순위

### 전체 진행 순서

```text
P0 테스트 보강 → P0 ECB 분리 → P1 SRP 분리 → P2 계약·중복·테스트 정렬 → P3 문서·cov
```

### 우선순위 매트릭스

| 우선순위 | 그룹 | 핵심 산출 | 완료 조건 |
|----------|------|-----------|-----------|
| **P0** | A → B | 테스트 net + Port/Adapter | 80+α passed, ECB 위반 해소 |
| **P1** | C-1 | resolver / formatter / presenter SRP | GM + AC 불변 |
| **P2** | C-2, D, E-1~2 | UI·CLI, 계약·상수, 테스트 경로·cov | GM diff 없음, cov gate |
| **P3** | E-3 | defect_list 동기화 | 문서 = pytest 상태 |

---

### 그룹 A — 테스트 선행 (회귀 안전망) · P0

> REFACTOR 코드 변경 **전** RED→GREEN 필수. `pytest.fail` RED 스켈레톤: **0건** (Dual-Track GREEN 완료).

| 상태 | ID | 대상 | 검증 / 조치 |
|------|-----|------|-------------|
| [x] | A-1 | `tests/control/test_magic_square_control.py` (신규) | `MagicSquareControl.solve()` — validate 실패 → resolver 0회; 통과 → 1회 |
| [x] | A-2 | `tests/control/test_magic_square_resolver.py` (신규) | `SolverNoSolutionError` → `ERR_SOLVER_NO_SOLUTION` / Control layer |
| [x] | A-3 | `test_ac_fr01_01_invalid_size.py` | TC-BND-006 (5×5), DET-001 (결정론×2), IMM-001 (grid 불변) |
| [x] | A-4 | `test_u_flow_domain_isolation.py` | range·duplicate 실패 시 resolver spy 0회 |
| [x] | A-5 | `test_u_out_result_format.py` | `to_int6()` negative — non-list, len≠6, 좌표 범위 → `ValueError` |
| [ ] | A-6 | `test_screen_presenter.py` (선택) | validate/solve 위임, `format_*` 문자열 |

---

### 그룹 B — ECB 아키텍처 (의존 방향) · P0

> **선행:** 그룹 A-1, A-2 GREEN

| 상태 | ID | 대상 | 문제 | 조치 |
|------|-----|------|------|------|
| [x] | B-1 | `control/magic_square_control.py` | `BoundaryValidator`, `ErrorResponse` 직접 import | `control/ports.py` — `ValidationPort`, Application DTO |
| [x] | B-2 | `control/magic_square_resolver.py` | `boundary.magic_square.contracts` import | Control 소유 DTO + Boundary adapter |
| [x] | B-3 | `boundary/magic_square/contracts.py` | DTO·에러 코드가 Boundary에만 존재 | Port 계약 이동, Boundary는 adapter |

---

### 그룹 C — SRP (함수·클래스 책임 분리)

#### C-1 Control / Boundary 핵심 · P1

> **선행:** 그룹 B 완료 권장

| 상태 | ID | 대상 | 문제 | 조치 |
|------|-----|------|------|------|
| [x] | C-1a | `control/magic_square_resolver.py:22` | Solver 호출 + ErrorResponse 조립 | `SolverErrorMapper` (Extract Class) |
| [x] | C-1b | `boundary/result_formatter.py:11` | 계약 검증 + int[6] 정규화 | `Int6ContractValidator` + Formatter 분리 |
| [x] | C-1c | `boundary/screen/presenter.py:12` | use-case 위임 + 출력 포맷 | `ViewFormatter` (Extract Class) |

#### C-2 UI / CLI · P2

> **선행:** C-1c (Presenter 분리 후 main_window 정리)

| 상태 | ID | 대상 | 문제 | 조치 |
|------|-----|------|------|------|
| [x] | C-2a | `boundary/screen/main_window.py:37,47` | Presenter 주입 + UI / 샘플 wiring 혼재 | Composition Root, `LayoutBuilder` |
| [ ] | C-2b | `boundary/cli/user_cli_boundary.py:21` | 파싱 + Control + dict 직렬화 | `_parse_*` / `_serialize_*` (Extract Method) |

---

### 그룹 D — 계약·상수·중복 정리 · P2

| 상태 | ID | 대상 | 문제 | 조치 |
|------|-----|------|------|------|
| [ ] | D-1 | `input_validator.py` / `boundary_validator.py` | Facade 중복 (OPEN-04) | 단일 진입점 통일 |
| [ ] | D-2 | `entity/constants.py` / `contracts.py` | `GRID_SIZE` 등 이중 정의 | entity SSOT → boundary re-export |
| [ ] | D-3 | `boundary/magic_square/contracts.py` | OPEN-01: `INVALID_SIZE` vs `ERR_INVALID_SHAPE` | PRD 명칭 통일 + GM baseline 재approve |
| [ ] | D-4 | `boundary/magic_square/boundary_validator.py` | `validate()` 단일 거대 함수 | A-3 GREEN 후 shape/blank/range/duplicate 메서드 추출 |

---

### 그룹 E — 테스트·문서 정렬 · P2 ~ P3

| 상태 | ID | 대상 | 문제 | 조치 | 우선순위 |
|------|-----|------|------|------|----------|
| [ ] | E-1 | `test_u_out_result_format.py` | `Solver()` 직접 호출 — Entity 우회 | Control + `ResultFormatter` E2E | P2 |
| [ ] | E-2 | `pytest.ini` / CI | cov threshold 미적용 | boundary/control 85%+, 전체 90%+ | P2 |
| [ ] | E-3 | `defect_list.md` | 80 passed와 불일치 | CLOSE/OPEN 상태 갱신 | P3 |

---

### 권장 실행 로드맵

```text
Phase 0 (P0)
  [ ] A-1 ~ A-5 GREEN
  [ ] B-1 ~ B-3 REFACTOR

Phase 1 (P1)
  [ ] C-1a ~ C-1c REFACTOR

Phase 2 (P2)
  [ ] D-1 ~ D-4
  [ ] C-2a, C-2b
  [ ] E-1, E-2
  [ ] (선택) A-6

Phase 3 (P3)
  [ ] E-3
```

### 리팩토링 후 검증

**회귀 테스트**

```powershell
python -m pytest tests/ -v
pytest -m golden_master -v
python -m pytest tests/control/ tests/boundary/ tests/integration/ -v
python -m pytest tests/ --cov=boundary --cov=control --cov=entity --cov-report=term-missing
```

**외부 동작 불변**

- Golden Master: `tests/golden_master_expected.txt` diff 없음
- GM-TC-01~05: int[6], row-major, 1-index, Error code/layer
- AC-FR-01-01 25건: 에러 code/message/layer 불변
- Domain 격리: FR-01 실패 시 `resolve` 0회

**Smoke**

```powershell
python -c "from boundary.screen.presenter import MagicSquareScreenPresenter; from boundary.screen.sample_grids import grid_reverse_success_sample; print(MagicSquareScreenPresenter().solve(grid_reverse_success_sample()))"
# [3, 3, 7, 4, 4, 1]

python scripts/generate_golden_master.py
git diff tests/golden_master_expected.txt
# diff 없음

python -m boundary.screen
```

---

## TDD 진행 체크리스트

> 기준: [test_plan.md](./test_plan.md) · [defect_list.md](./defect_list.md)  
> 표기: **RED** = 실패 테스트 작성 · **GREEN** = 최소 구현 통과 · `[ ]` = 미완 · `[x]` = 완료

### AC-FR-01-01 — 형태 검증 (I-1) · `test_ac_fr01_01_invalid_size.py`

| 상태 | TC | 내용 |
|------|-----|------|
| [x] GREEN | TC-A-01 | `grid=None` → `INVALID_SIZE` / `Grid must be 4x4.` |
| [x] GREEN | TC-A-02 | `code == "INVALID_SIZE"` 문자열 일치 |
| [x] GREEN | TC-A-03 | `message` 문자 단위 일치 |
| [x] GREEN | TC-A-04 | `grid=None` 시 `resolve()` 0회 (spy) |
| [x] GREEN | TC-A-05 | `grid=[]` → 실패 |
| [x] GREEN | TC-A-06 | 3×4 / 4×3 크기 불일치 → 실패 |
| [x] GREEN | TC-A-07 | 반환 타입 `ErrorResponse` (pydantic) |
| [x] GREEN | TC-B-01~03 | 형태 실패 시 Domain 격리 (`TestAcFr0101DomainIsolation`) |
| [x] GREEN | TC-B-04 | AC-FR-01-02~05 오류 코드 미반환 확인 (`TestAcFr0101ScopeRestriction`) |
| [x] GREEN | — | 메시지 동일성·layer=Boundary (동 파일 25건 전체 통과) |
| [x] GREEN | TC-BND-006 | 5×5 행렬 → `INVALID_SIZE` |
| [x] GREEN | TC-BND-DET-001 | `validate` ×2 결정론 |
| [x] GREEN | TC-BND-IMM-001 | validate 전후 grid 불변 |

**실행:** `python -m pytest tests/boundary/test_ac_fr01_01_invalid_size.py -v` → **28 passed**

### Track A — Boundary / Control (GREEN 완료 9건)

| 상태 | TC ID | 테스트 파일 | 내용 | AC |
|------|-------|-------------|------|-----|
| [x] GREEN | U-IN-04 | `test_u_in_input_validation.py` | 빈칸 0개 → `ERR_INVALID_BLANK_COUNT` | AC-FR01-02 |
| [x] GREEN | U-IN-05 | 동일 | 빈칸 1개 → `ERR_INVALID_BLANK_COUNT` | AC-FR01-02 |
| [x] GREEN | U-IN-06 | 동일 | 빈칸 3개 → `ERR_INVALID_BLANK_COUNT` | AC-FR01-02 |
| [x] GREEN | U-IN-07 | 동일 | 값 17 → `ERR_OUT_OF_RANGE` | AC-FR01-03 |
| [x] GREEN | U-IN-08 | 동일 | non-zero 중복 → `ERR_DUPLICATE_VALUE` | AC-FR01-04 |
| [x] GREEN | U-FLOW-02 | `test_u_flow_domain_isolation.py` | blank-count 실패 시 Domain 0회 | BR-05 |
| [x] GREEN | U-OUT-01 | `test_u_out_result_format.py` | 성공 payload `len == 6` | AC-FR05-04 |
| [x] GREEN | U-OUT-02 | 동일 | 좌표 1-indexed (1..4) | AC-FR05-05 |
| [x] GREEN | U-OUT-03 | 동일 | reverse `[3,3,7,4,4,1]` (TD-01) | AC-FR05-02 |

### Track B — Domain / Entity (GREEN 완료 12건)

| 상태 | TC ID | 테스트 파일 | 내용 | FR |
|------|-------|-------------|------|-----|
| [x] GREEN | D-LOC-01 | `test_d_loc_blank_finder.py` | `BlankFinder` row-major 2좌표 | FR-02 |
| [x] GREEN | D-MIS-01 | `test_d_mis_missing_number_finder.py` | `MissingNumberFinder` [small, large] | FR-03 |
| [x] GREEN | D-VAL-01 | `test_d_val_magic_square_validator.py` | 행 합 = 34 | FR-04 |
| [x] GREEN | D-VAL-02 | 동일 | 열 합 = 34 | FR-04 |
| [x] GREEN | D-VAL-03 | 동일 | 주대각 합 = 34 | FR-04 |
| [x] GREEN | D-VAL-04 | 동일 | 부대각 합 = 34 | FR-04 |
| [x] GREEN | D-VAL-05 | 동일 | 완전 마방진 → valid | FR-04 |
| [x] GREEN | D-VAL-06 | 동일 | 한 줄 합 ≠ 34 → invalid | FR-04 |
| [x] GREEN | D-SOL-01 | `test_d_sol_solver.py` | reverse `[3,3,7,4,4,1]` | FR-05 |
| [x] GREEN | D-SOL-02 | 동일 | small-first `[3,2,6,3,3,7]` | FR-05 |
| [x] GREEN | D-SOL-03 | 동일 | 두 조합 실패 → `SolverNoSolutionError` | FR-05 |
| [x] GREEN | D-SOL-04 | 동일 | solve 후 입력 grid 불변 | FR-05 |

### 커버리지 목표

- [ ] Domain Logic: 95%+ (`pytest-cov`)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결

- [x] defect_list.md 생성 — [defect_list.md](./defect_list.md)
- [x] DEF-001~005 CLOSE — AC-FR-01-01 GREEN (`test_ac_fr01_01_invalid_size.py` 25 passed)
- [x] DEF-006 이후 · Track A/B 스켈레톤 — Dual-Track GREEN 완료
- [x] Golden Master GM-1~2 — `pytest -m golden_master` → **18 passed**
- [x] 전체 회귀 `python -m pytest tests/` → **80 passed**

---

## 문서 인덱스

| 문서 | 설명 | 작성일 |
|------|------|--------|
| [Report/01 — 문제 정의](./Report/01MagicSquare-Problem-Definition-Report.md) | STEP 1~5 통합 (Invariant I-1~I-10) | 2026-05-28 |
| [Report/02 — TDD 설계](./Report/02MagicSquare-TDD-Design-Report.md) | 판정 1차·생성 2차, P0 시나리오 | 2026-05-28 |
| [Report/03 — ECB User 구현](./Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md) | Cursor Rule + User 수직 슬라이스 | 2026-05-28 |
| [Report/04 — 규칙 확장](./Report/04MagicSquare-Rule-Expansion-and-Prompt-Export-Report.md) | .mdc 분할, Prompt 경로 통일 | 2026-05-28 |
| [Report/05 — TODO Web 스택](./Report/05TodoWeb-Stack-Recommendation-Report.md) | React+TS+Vite 권장 (참고용) | 2026-05-28 |
| [Report/06 — Journey/Story/Scenario](./Report/06MagicSquare-UserJourney-Story-Scenario-Report.md) | Epic~Level 4 시나리오 | 2026-05-28 |
| [Report/07 — PRD 작성·검토](./Report/07MagicSquare-PRD-Development-and-Review-Report.md) | PRD 산출 + 7기준 검토 | 2026-05-29 |
| [Report/08 — TDD 시작·To-Do](./Report/08MagicSquare-TDD-Start-ToDo-README-Report.md) | 샘플 AC-FR01-01 선정·추적 보드·README RED To-Do | 2026-05-29 |
| [Report/09 — AC-FR01-01 RED·HTML](./Report/09MagicSquare-AC-FR01-01-RED-Test-HTML-Report.md) | RED 25건·venv·HTML·[defect_list.md](./defect_list.md) | 2026-05-29 |
| [Report/10 — Dual-Track RED Skeleton](./Report/10MagicSquare-DualTrack-RED-Skeleton-Report.md) | U-IN/U-OUT/U-FLOW·D-* 스켈레톤 21건 | 2026-05-29 |
| [Report/11 — AC-FR01-01 GREEN](./Report/11MagicSquare-AC-FR01-01-GREEN-Report.md) | I-1 GREEN 25건·체크리스트·21 failed 분석 | 2026-05-29 |
| [Report/12 — Dual-Track GREEN + PyQt](./Report/12MagicSquare-DualTrack-GREEN-PyQt-Report.md) | 21건 GREEN·62 passed·PyQt GUI | 2026-05-29 |
| [Report/14 — Golden Master 회귀](./Report/14MagicSquare-GoldenMaster-Regression-Report.md) | GM-1~3·approve·80 passed·GM-TC-01~05 | 2026-05-29 |
| [Report/15 — REFACTOR 계획](./Report/15MagicSquare-REFACTOR-Plan-Report.md) | 코드 리뷰·SRP·테스트 선행·REFACTOR 로드맵 | 2026-05-29 |
| [docs/PRD_MagicSquare.md](./docs/PRD_MagicSquare.md) | 구현 전 PRD 본문 (23개 섹션) | 2026-05-29 |
| [docs/README.md](./docs/README.md) | docs 인덱스 · RED To-Do · Golden Master (GM-1~3) | 2026-05-29 |
| [docs/golden_master_approval_design.md](./docs/golden_master_approval_design.md) | Golden Master approve 패턴 설계 | 2026-05-29 |
| [Report/README.md](./Report/README.md) | Report 폴더 목차 | — |

---

## 라이선스

미정 (추가 예정)
