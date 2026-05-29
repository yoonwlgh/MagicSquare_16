# Magic Square — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **문서 ID** | DL-MS-001 |
| **버전** | 0.1 |
| **기준일** | 2026-05-29 |
| **출처** | `pytest tests/` (41 collected), `report/pytest_report.html`, AC-FR-01-01 RED 스위트 |
| **상태** | OPEN 5건 / CLOSED 0건 — GREEN 미착수 |

---

## 요약

| 구분 | 수치 |
|------|------|
| pytest 실패 | **24** (AC-FR-01-01) |
| pytest 통과 | **17** (User ECB 16 + scope 메타 1) |
| 근본 결함 (고유) | **5** |
| Critical | **5** |

> 24개 실패 테스트는 아래 **5개 근본 결함**에 매핑된다. 동일 원인으로 실패한 테스트는 「영향 테스트」에만 열거한다.

---

## 결함 등록표

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| **DEF-001** | Critical | AC-FR-01-01 | 1. `BoundaryValidator()` 생성 2. `validate(grid=None)` 호출 | `ErrorResponse(code="INVALID_SIZE", message="Grid must be 4x4.", layer="Boundary")` | `None` (`isinstance(result, ErrorResponse)` → False) | `BoundaryValidator.validate` RED 스텁 — 입력 미검사, 항상 `return None` | `grid is None` 및 형태 비성립 시 `ErrorResponse(INVALID_SIZE, …)` 반환 |
| **DEF-002** | Critical | AC-FR-01-01 | 1. `validate(grid=[])` 호출 | 동일 `INVALID_SIZE` 계열 `ErrorResponse` | `None` | 빈 리스트(0행)에 대한 4×4 형태 검사(I-1) 미구현 | 행 수·열 수 검사 추가; `len(grid) != 4` 시 즉시 실패 반환 |
| **DEF-003** | Critical | AC-FR-01-01 | 1. `validate(grid=[[]]*4)` 또는 `validate(grid=[[],[],[],[]])` 호출 | `INVALID_SIZE` `ErrorResponse` | `None` | 「4행이나 열 길이 0」 패턴 미검출 | 각 행 `len(row) == 4` 검증; 0열·가변 열 길이 시 실패 반환 |
| **DEF-004** | Critical | AC-FR-01-01 | 1. `validate(grid=3×4)` — `[[1]*4,[2]*4,[3]*4]` 2. 또는 `validate(grid=4×3)` | `INVALID_SIZE` `ErrorResponse` | `None` | 3×4·4×3·5×5 등 크기 불일치 행렬 미검출 | `GRID_SIZE=4` 상수로 행·열 개수 일치 검사 |
| **DEF-005** | Critical | AC-FR-01-01, BR-05 | 1. `MagicSquareControl(boundary_validator, resolver=MagicMock())` 2. `solve(grid=None)` 호출 3. `resolver.resolve.call_count` 확인 | `call_count == 0`; 반환값은 `ErrorResponse` | `call_count >= 1` (검증 통과로 간주 후 `resolve(None)` 호출); 반환값 `MagicMock` | DEF-001 연쇄 — `validate`가 `None` 반환 → Control이 성공 경로로 `resolve()` 호출 (BR-05·EP-01 위반) | `validate` 실패 시 `ErrorResponse` 즉시 반환; `resolve()` 호출 금지 |

---

## 영향 테스트 매핑

### DEF-001 — `grid=None` / 메시지·타입·범위 코드

| 테스트 ID | 테스트 함수 (요약) |
|-----------|-------------------|
| TC-A-01 | `test_grid_none_returns_invalid_size_error_response` |
| TC-A-02 | `test_grid_none_failure_code_is_invalid_size_string` |
| TC-A-03 | `test_grid_none_failure_message_is_grid_must_be_4x4` |
| TC-A-07 | `test_grid_none_returns_pydantic_error_response_model` |
| — | `test_grid_none_failure_layer_is_boundary` |
| — | `test_grid_none_message_exact_prd_contract_string` |
| — | `test_grid_none_does_not_return_blank_count_error_code` |
| — | `test_grid_none_does_not_return_out_of_range_error_code` |
| — | `test_grid_none_does_not_return_duplicate_value_error_code` |
| — | `test_grid_none_invalid_size_not_in_forbidden_solver_codes` |

### DEF-002 — `grid=[]`

| 테스트 ID | 테스트 함수 (요약) |
|-----------|-------------------|
| TC-A-05 | `test_grid_empty_list_returns_invalid_size_failure` |
| — | `test_grid_empty_list_message_character_for_character_match` |

### DEF-003 — `grid=[[]]*4` / 4×빈 행

| 테스트 ID | 테스트 함수 (요약) |
|-----------|-------------------|
| — | `test_grid_four_empty_rows_returns_invalid_size_failure` |
| — | `test_grid_four_empty_rows_via_repeat_pattern_returns_invalid_size` |
| — | `test_grid_four_empty_rows_message_no_extra_whitespace` |
| — | `test_grid_repeat_empty_rows_message_byte_identity` |

### DEF-004 — 3×4 / 4×3

| 테스트 ID | 테스트 함수 (요약) |
|-----------|-------------------|
| TC-A-06 | `test_grid_3x4_matrix_returns_invalid_size_failure` |
| — | `test_grid_4x3_matrix_returns_invalid_size_failure` |
| — | `test_grid_3x4_message_equals_invalid_size_constant` |

### DEF-005 — Domain `resolve()` 격리

| 테스트 ID | 테스트 함수 (요약) |
|-----------|-------------------|
| TC-A-04 | `test_grid_none_resolve_call_count_zero` |
| TC-B-01~03 | `test_grid_*_resolve_*` (None, `[]`, 4×빈행, 3×4) |
| — | `test_grid_none_solve_returns_boundary_error_without_resolve` |

---

## 커버리지 관련 관찰 (결함 후보)

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| **DEF-006** | Low | AC-FR-01-01 | `pytest --cov=control` 후 `magic_square_control.py` line 35 확인 | 검증 실패 분기 실행·커버 | line 35 `return validation_error` **미실행** (Miss) | DEF-001·005 — 실패 분기가 호출되지 않음 | DEF-001~005 수정 시 자동 해소 예상; 별도 수정 불필요 |

---

## 수정 우선순위 (GREEN 권장 순서)

```text
1. DEF-001  (None → INVALID_SIZE)     — RED-BND-001 앵커
2. DEF-002~004 (형태 검사 통합)       — 동일 validate() 내 I-1
3. DEF-005  (resolve 격리)            — RED-BND-ISO-001
4. DEF-006  (커버리지)                — 회귀 확인만
```

---

## 검증 기준 (결함 CLOSE 조건)

- [ ] `python -m pytest tests/boundary/test_ac_fr01_01_invalid_size.py` → **25 passed**
- [ ] `python -m pytest tests/` → **41 passed** (User 슬라이스 회귀 포함)
- [ ] README RED To-Do TC-A-01 ~ TC-A-07, TC-B-01 ~ TC-B-03 체크 가능
- [ ] `report/pytest_report.html` 재생성 시 Failed 0

---

## 참고

| 문서 | 경로 |
|------|------|
| 테스트 플랜 | `test_plan.md` |
| RED 보고서 | `Report/09MagicSquare-AC-FR01-01-RED-Test-HTML-Report.md` |
| 구현 대상 | `boundary/magic_square/boundary_validator.py`, `control/magic_square_control.py` |
| OPEN-01 | `INVALID_SIZE` vs PRD `ERR_INVALID_SHAPE` 명칭 통일 (수정 시 상수 한곳 정의) |
