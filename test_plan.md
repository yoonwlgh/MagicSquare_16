# Magic Square 4×4 — 테스트 계획서 (Test Plan)

| 항목 | 내용 |
|------|------|
| **문서 ID** | TP-MS-001 |
| **버전** | 0.1 (AC-FR01-01 선행 스코프) |
| **작성 기준** | PRD `docs/PRD_MagicSquare.md`, Report/02 S-011, Report/08 샘플 선정 |
| **대상 런타임** | Python 3.11+ |
| **테스트 스택** | pytest, pydantic, unittest.mock |
| **앵커 AC** | **AC-FR01-01** — 입력 형태 비성립 (I-1 선행) |
| **앵커 시나리오** | **SC-BND-001** / **S-011** — `grid = None` |
| **앵커 RED** | **RED-BND-001** (형태 거부), **RED-BND-ISO-001** (Domain 미호출) |

---

## 1. 목적 및 범위

본 계획서는 샘플 예제 **AC-FR01-01** (`grid=None` → 형태 오류)를 중심으로, **FR-01 Boundary 입력 검증**의 pytest 단위 테스트 범위·우선순위·경계값·격리 전략·커버리지 게이트를 정의한다.

### 1.1 In Scope (본 문서 1차)

- `BoundaryValidator`(또는 동등 Boundary 컴포넌트)의 **형태/존재 검사(I-1)** 단위 테스트
- 구조화 Error Response 계약 (`code`, `message`, `layer`)
- Boundary 실패 시 **Domain Solver 파이프라인 미호출**(BR-05, EP-01)
- pytest-cov 기반 Boundary/Domain 커버리지 측정 전략

### 1.2 Out of Scope (본 문서 1차 — 명시적 제외)

| 제외 항목 | 이유 | 후속 AC/RED |
|-----------|------|-------------|
| **4×4 정상 입력** (빈칸 2개·값 규칙 충족) | AC-FR01-01 범위 외; 형태 검증 통과 후속 단계 | AC-FR01-05, FR-02~05 |
| 빈칸 개수·값 범위·중복 검증 상세 | I-2, I-3 선행 조건 미충족 입력만 본 1차 RED | AC-FR01-02~04 |
| Solver 성공/실패·`int[6]` 포맷 | Control/Domain Track B | FR-05, RED-BND-008~009 |
| UI/CLI/DB/Web | PRD OS-01~03 | — |

> **계약 표기:** 테스트 플랜 샘플은 `INVALID_SIZE` / `Grid must be 4x4.` 를 사용한다. PRD §13.2 공식 코드는 `ERR_INVALID_SHAPE` / `Input must be a 4x4 integer matrix.` 이다. RED 착수 전 **OPEN-01**으로 단일 enum/상수로 매핑한다.

---

## 2. 추적 매트릭스 (앵커)

| 계층 | ID | Given | When | Then |
|------|-----|-------|------|------|
| AC | **AC-FR01-01** | 형태 비성립 `grid` | `BoundaryValidator.validate(grid)` | `INVALID_SIZE`(또는 매핑된 `ERR_INVALID_SHAPE`), Domain **0회** 호출 |
| Scenario | **SC-BND-001** | `grid is None` | validate | 동일 |
| Report/02 | **S-011** | null/빈 배열/비정수 포함(1차는 null·형태 위주) | 거부 | 무효, I-1 |
| PRD | **FR-01**, §12.1, §13.2, §16.2 **ES-01** | 4×4 아님 | validate | Error, Domain No |
| BR | **BR-01**, **BR-05** | 4×4 형태 위반 / 검증 실패 | — | 즉시 실패, Solver 미호출 |
| EP | **EP-01** | 입력 검증 실패 | — | BlankFinder, MissingNumberFinder, Solver 미호출 |

---

## 3. pytest 단위 테스트 범위 및 우선순위

### 3.1 테스트 디렉터리 (ECB 미러)

| 우선순위 | 경로 (계획) | 대상 컴포넌트 | Track | 비고 |
|----------|-------------|---------------|-------|------|
| **P0** | `tests/boundary/test_boundary_validator.py` | `BoundaryValidator` | A (FR-01) | 본 계획서 핵심 |
| **P0** | `tests/boundary/test_boundary_domain_isolation.py` | Control 진입 + mock/spy | A | RED-BND-ISO-001 |
| P1 | `tests/entity/test_blank_finder.py` | `BlankFinder` | B (FR-02) | FR-01 GREEN 후 |
| P1 | `tests/entity/test_missing_number_finder.py` | `MissingNumberFinder` | B (FR-03) | 동일 |
| P1 | `tests/entity/test_magic_square_validator.py` | `MagicSquareValidator` | B (FR-04) | 동일 |
| P2 | `tests/entity/test_solver.py` | `Solver` | B (FR-05) | Control RED와 교차 |
| P2 | `tests/control/test_solve_orchestration.py` | Control use-case | Control | 통합에 가까움; 단위는 mock Domain |

### 3.2 우선순위 정의 (RED 착수 순서)

```text
P0-1  RED-BND-001  grid=None          → INVALID_SIZE + layer=Boundary
P0-2  RED-BND-002  크기 불일치 행렬   → 동일 Error family (AC-FR01-01 확장)
P0-3  RED-BND-ISO-001  모든 P0-1~2 케이스에서 Domain 파이프라인 call_count == 0
P1    AC-FR01-02~04   (빈칸/범위/중복) — 본 문서 §4 이후 스프린트
P2    Track B Domain 단위 + Control 조율
```

### 3.3 테스트 작성 규칙

- **AAA** (Arrange / Act / Assert) 필수; 함수명 `test_` 접두사.
- **Dual-Track:** Track A(Boundary) RED와 Track B(Domain) RED는 파일·픽스처 분리.
- **TDD:** RED(의도된 실패 확인) → GREEN(최소 구현) → REFACTOR; RED 확인 전 production 구현 금지.
- **금지:** `print()` 디버깅, bare `except`, skip/ assertion 삭제로 통과, 4×4 정상 격자를 AC-FR01-01 스위트에 포함.

### 3.4 pydantic 역할

| 모델 (계획) | 용도 |
|-------------|------|
| `ErrorResponse` | `code`, `message`, `layer` 필드 고정; Boundary 실패 응답 역직렬화 검증 |
| `ValidationResult` (선택) | success / error 분기; Boundary 단위 테스트에서 타입 안정성 확보 |

단위 테스트에서는 `ErrorResponse.model_validate(result)` 또는 동등 생성자로 **계약 필드 누락**을 조기에 탐지한다.

---

## 4. 경계값 케이스 목록 (AC-FR01-01 / I-1)

모든 케이스는 **동일 기대 Error family** 를 가정한다 (플랜 샘플 표기 기준).

| Case ID | 입력 `grid` | 기대 `code` | 기대 `message` (샘플) | Domain 호출 | RED ID | AC-FR01-01 포함 |
|---------|-------------|-------------|------------------------|-------------|--------|-----------------|
| **BV-001** | `None` | `INVALID_SIZE` | `Grid must be 4x4.` | 0 | RED-BND-001 | **예 (앵커)** |
| **BV-002** | `[]` | `INVALID_SIZE` | 동일 | 0 | RED-BND-001 | 예 |
| **BV-003** | `[[]] * 4` | `INVALID_SIZE` | 동일 | 0 | RED-BND-001 | 예 (4행, 열 길이 0) |
| **BV-004** | `3×4` 행렬 (3행×4열) | `INVALID_SIZE` | 동일 | 0 | RED-BND-002 | 예 |
| **BV-005** | `4×3` 행렬 (4행×3열) | `INVALID_SIZE` | 동일 | 0 | RED-BND-002 | 예 |
| **BV-006** | `5×5` 행렬 (5행×5열) | `INVALID_SIZE` | 동일 | 0 | RED-BND-002 | 예 |
| — | **4×4 정상 입력** (예: 빈칸 2개 규칙 충족) | — | — | — | — | **포함 금지** |

### 4.1 BV-004~006 입력 구성 가이드 (Arrange)

- **BV-004 (3×4):** `[[1]*4, [2]*4, [3]*4]` — 행 3, 열 4.
- **BV-005 (4×3):** `[[1,2,3], [4,5,6], [7,8,9], [10,11,12]]` — 행 4, 열 3.
- **BV-006 (5×5):** 5행 각각 길이 5인 정수 리스트 (값은 형태 검증만 목적이면 placeholder 허용).

### 4.2 검사 순서 (Fail-Fast) 계약

형태 검사는 **I-1 선행**이다. BV-001~006에서 Boundary는 빈칸 개수(BR-02)·값 범위(BR-03)·중복(BR-04) 로직에 **진입하지 않아야** 한다 (내부 early-return 또는 단일 `validate_shape` 단계로 관측 가능).

### 4.3 BV-003 특이 주의 (`[[]] * 4`)

Python에서 `[[]] * 4`는 4개 행이 **동일 빈 리스트 객체를 참조**할 수 있다. 본 케이스의 목적은 **「열 없음」 형태 거부**이지, 이후 변형(mutate) 시나리오가 아니다. 테스트는 **검증 직전 스냅샷**만 사용하고, 행렬 변형 부작용 검증은 §5 예외 케이스로 분리한다.

---

## 5. 예외·특이 케이스 목록

| Case ID | 분류 | 입력/조건 | 기대 동작 | 비고 |
|---------|------|-----------|-----------|------|
| **EX-001** | 타입 오류 | `grid = "not a grid"` (str) | `INVALID_SIZE` (또는 전용 타입 코드 — OPEN-01) | AC-FR01-01 확장; pydantic 전처리 시 ValidationError 매핑 정책 고정 |
| **EX-002** | 타입 오류 | `grid = 123` (int) | 동일 | iterable 아님 |
| **EX-003** | 혼합 행 길이 | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | `INVALID_SIZE` | 4행이나 열 수 불일치 (Report/02 S-008 계열) |
| **EX-004** | 빈 행 리스트 | `[[], [], [], []]` | `INVALID_SIZE` | BV-003과 구분: 명시적 4×0 |
| **EX-005** | 결정론 | BV-001 동일 입력 2회 `validate` | 동일 `code`/`message` | NFR-03, I-9 |
| **EX-006** | 부작용 없음 | BV-001~003 실행 전후 `grid` id/내용 동일 | 입력 불변 | NFR-04, EP-04 |
| **EX-007** | 격리 회귀 | BV-001 + Control `solve` mock | Domain 스텁 **0회** | RED-BND-ISO-001; FR-01 실패가 FR-05로 누수되지 않음 |
| **EX-008** | 명시적 제외 확인 | 4×4 + 빈칸 2개 유효 격자 | **본 스위트 미실행** | AC-FR01-05 / 별도 `tests/` 파일 |

---

## 6. Domain 해 결정 진입점 호출 횟수 검증 전략 (mock / spy)

### 6.1 검증 대상 (EP-01, BR-05)

PRD상 입력 검증 실패 시 호출되지 않아야 하는 **Domain Solver 파이프라인** 진입점:

| 진입점 (계획 명) | 모듈 (계획) | FR | mock 대상 메서드 (예) |
|------------------|-------------|-----|------------------------|
| `BlankFinder.find_blanks` | `entity/blank_finder.py` | FR-02 | `find_blanks` |
| `MissingNumberFinder.find_missing` | `entity/missing_number_finder.py` | FR-03 | `find_missing` |
| `MagicSquareValidator.is_valid` | `entity/magic_square_validator.py` | FR-04 | `is_valid` |
| `Solver.solve` | `entity/solver.py` | FR-05 | `solve` |

**Control 단일 진입점(권장 spy 지점):** `control.magic_square_control.solve(grid)` — 내부에서 위 4종을 순차 호출한다고 가정한다.

### 6.2 전략 A — Control 경유 격리 테스트 (권장, RED-BND-ISO-001)

```python
# 개념 스케치 (구현은 RED 단계에서 tests/boundary/ 에 작성)
from unittest.mock import MagicMock, patch

def test_validate_invalid_grid_does_not_invoke_domain_pipeline():
    # Arrange
    invalid_grid = None
    blank_finder = MagicMock()
    missing_finder = MagicMock()
    validator = MagicMock()
    solver = MagicMock()
    control = MagicSquareControl(
        boundary_validator=BoundaryValidator(),
        blank_finder=blank_finder,
        missing_finder=missing_finder,
        validator=validator,
        solver=solver,
    )

    # Act
    result = control.solve(grid=invalid_grid)

    # Assert — Boundary 계약
    assert result.code == "INVALID_SIZE"
    assert result.message == "Grid must be 4x4."
    assert result.layer == "Boundary"
    # Assert — 호출 횟수
    blank_finder.find_blanks.assert_not_called()
    missing_finder.find_missing.assert_not_called()
    validator.is_valid.assert_not_called()
    solver.solve.assert_not_called()
```

| 검증 항목 | 기대 |
|-----------|------|
| `find_blanks.call_count` | `0` |
| `find_missing.call_count` | `0` |
| `is_valid.call_count` | `0` |
| `solve.call_count` | `0` |

**적용 케이스:** BV-001 ~ BV-006 전부에 대해 동일 패턴 파라미터화(`@pytest.mark.parametrize`).

### 6.3 전략 B — Boundary 단독 단위 (RED-BND-001)

`BoundaryValidator.validate` 단위 테스트에서는 Domain 모듈이 **import 되지 않도록** 설계한다 (ECB: `boundary` → `control` → `entity`, `boundary` ↛ `entity` 직접 참조 금지).

- Domain mock **불필요** — 아키텍처 의존성 테스트로 격리 보조.
- Error Response 필드만 assert.

### 6.4 전략 C — `patch` 스파이 (대안)

Control 내부가 아직 미구현일 때, 모듈 경로에 `patch("entity.blank_finder.BlankFinder.find_blanks")` 등을 사용해 **실수로 로드된 경우**도 호출 0을 보장한다. REFACTOR 시 전략 A로 수렴 권장.

### 6.5 실패 시 진단 기준

| 관측 | 판정 |
|------|------|
| Domain mock 1회 이상 호출 | BR-05 위반 — **FAIL** |
| Error `layer` ≠ `"Boundary"` | Boundary/Domain 책임 혼입 — **FAIL** |
| 4×4 유효 입력이 AC-FR01-01 파일에서 GREEN | 범위 침범 — 테스트 이동 필요 |

---

## 7. 커버리지 목표

| 계층 | NFR | 목표 | 측정 대상 (계획 패키지) |
|------|-----|------|-------------------------|
| **Domain (Entity)** | NFR-01 | **≥ 95%** | `entity/` (BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver) |
| **Boundary** | NFR-02 | **≥ 85%** | `boundary/` (BoundaryValidator, CLI/API adapter) |
| **Control** | — | ≥ 85% (권장) | `control/` (use-case 조율; FR-05 분기) |

### 7.1 본 스프린트(AC-FR01-01) 최소 게이트

- **BoundaryValidator** 형태 검사 분기(BV-001~006): **line/branch 100%** (해당 모듈 내 I-1 경로).
- Domain 모듈: AC-FR01-01 스프린트만으로 95% 달성 불필요 → **Track B RED 시작 시** Domain 95% 게이트 적용.

### 7.2 게이트 실패 시 조치

- 커버리지 미달: 해당 계층 RED 테스트 추가 (assertion 완화 금지, DT-05).
- Boundary에 Domain 로직이 잡히면 리팩터 후 재측정 (NFR-06).

---

## 8. pytest-cov 측정 전략

### 8.1 설치

```bash
pip install pytest pytest-cov pydantic
```

### 8.2 실행 (요청 표준 커맨드)

저장소가 `src/` 레이아웃을 채택한 경우:

```bash
pytest --cov=src --cov-report=term-missing
```

현재 ECB 루트 레이아웃(`boundary/`, `control/`, `entity/`) 병행 시:

```bash
pytest --cov=boundary --cov=control --cov=entity --cov-report=term-missing --cov-fail-under=85
```

Domain 95% 게이트 (Track B 착수 후):

```bash
pytest --cov=entity --cov-report=term-missing --cov-fail-under=95
```

### 8.3 권장 `pyproject.toml` / `pytest.ini` 스니펫 (계획)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -ra --strict-markers

[coverage:run]
source = boundary, control, entity
# src 레이아웃 전환 시: source = src

[coverage:report]
fail_under = 85
show_missing = True
```

### 8.4 AC-FR01-01 스위트만 부분 실행

```bash
pytest tests/boundary/test_boundary_validator.py -k "invalid_size or none or shape" --cov=boundary --cov-report=term-missing
```

### 8.5 리포트 해석

- `term-missing`: I-1 분기 누락 라인을 RED 추가 위치로 사용.
- Boundary 85%는 **전체 `boundary/` 패키지** 기준; AC-FR01-01만으로 달성 시에도 Track A 완료로 간주하지 않고, FR-01 전체 RED-BND-001~005 완료 후 최종 판정.

---

## 9. 테스트 케이스 명세 (AC-FR01-01 앵커 + 경계값)

| Test ID | Case | Arrange | Act | Assert |
|---------|------|---------|-----|--------|
| **TC-BND-001** | BV-001 | `grid=None` | `BoundaryValidator.validate(grid)` | `code==INVALID_SIZE`, `message` 일치, `layer==Boundary` |
| **TC-BND-002** | BV-002 | `grid=[]` | 동일 | 동일 |
| **TC-BND-003** | BV-003 | `grid=[[]]*4` | 동일 | 동일 |
| **TC-BND-004** | BV-004 | 3×4 matrix | 동일 | 동일 |
| **TC-BND-005** | BV-005 | 4×3 matrix | 동일 | 동일 |
| **TC-BND-006** | BV-006 | 5×5 matrix | 동일 | 동일 |
| **TC-ISO-001** | BV-001~006 | 각 grid + Domain mocks | `control.solve(grid)` | 4 Domain 진입점 `call_count==0` |
| **TC-BND-DET-001** | EX-005 | BV-001 | `validate` ×2 | 동일 결과 |
| **TC-BND-IMM-001** | EX-006 | mutable grid | validate 전후 | 입력 동일 |

---

## 10. 완료 기준 (Definition of Done — 본 계획 스코프)

- [ ] BV-001~006 pytest RED 확인 후 GREEN (최소 `validate_shape` / None 분기).
- [ ] TC-ISO-001: BV 전 케이스 Domain `call_count == 0`.
- [ ] pydantic `ErrorResponse` 계약 필드 검증 통과.
- [ ] 4×4 정상 입력 테스트가 **본 스위트 파일에 없음** (EX-008).
- [ ] `pytest --cov=boundary --cov-report=term-missing` 실행 기록; BoundaryValidator I-1 분기 missing 0.
- [ ] OPEN-01: `INVALID_SIZE` ↔ `ERR_INVALID_SHAPE` 매핑 문서·코드 일치.

---

## 11. 참고 문서

| 문서 | 경로 |
|------|------|
| PRD | `docs/PRD_MagicSquare.md` — FR-01, §12~13, §15~16, NFR-01~02 |
| TDD 설계 | `Report/02MagicSquare-TDD-Design-Report.md` — I-1, S-011 |
| TDD Start | `Report/08MagicSquare-TDD-Start-ToDo-README-Report.md` — RED-BND-001, OPEN-01 |
| ECB 규칙 | `.cursor/rules/magicsquare-ecb-architecture.mdc` |
| TDD 규칙 | `.cursor/rules/magicsquare-tdd-testing.mdc` |

---

*문서 끝 — 구현·테스트 코드는 본 계획서 승인 후 RED 단계에서 `tests/boundary/`에 추가한다.*
