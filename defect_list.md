# Magic Square — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **문서 ID** | DL-MS-001 |
| **버전** | 0.2 |
| **기준일** | 2026-05-29 |
| **출처** | `pytest tests/` (93 collected), AC-FR-01-01 GREEN · REFACTOR E-3 |
| **상태** | OPEN 0건 / CLOSED 6건 |

---

## 요약

| 구분 | 수치 |
|------|------|
| pytest 실패 | **0** |
| pytest 통과 | **93** (`pytest -m golden_master` → 18) |
| 근본 결함 (고유) | **6** (DEF-001 ~ DEF-006) |
| Critical | **5** (모두 CLOSE) |

> DEF-001 ~ DEF-005는 AC-FR-01-01 GREEN 및 Control 격리 테스트로 해소됨. DEF-006은 동일 수정으로 커버리지 분기 해소.

---

## 결함 등록표

| ID | Severity | AC ID | 상태 | CLOSE 근거 |
|----|----------|-------|------|------------|
| **DEF-001** | Critical | AC-FR-01-01 | **CLOSED** | `grid=None` → `ERR_INVALID_SHAPE` / Boundary layer |
| **DEF-002** | Critical | AC-FR-01-01 | **CLOSED** | `grid=[]` 형태 검사 |
| **DEF-003** | Critical | AC-FR-01-01 | **CLOSED** | `[[]]*4` 열 길이 검사 |
| **DEF-004** | Critical | AC-FR-01-01 | **CLOSED** | 3×4·4×3·5×5 `ERR_INVALID_SHAPE` |
| **DEF-005** | Critical | AC-FR-01-01, BR-05 | **CLOSED** | `solve()` 실패 시 `resolve()` 0회 |
| **DEF-006** | Low | AC-FR-01-01 | **CLOSED** | `magic_square_control` 검증 실패 분기 커버 |

---

## 검증 기준 (결함 CLOSE 조건)

- [x] `python -m pytest tests/boundary/test_ac_fr01_01_invalid_size.py` → **28 passed**
- [x] `python -m pytest tests/` → **93 passed**
- [x] `pytest -m golden_master` → **18 passed**
- [x] OPEN-01: `ERR_INVALID_SHAPE` / `Input must be a 4x4 integer matrix.` (D-3)

---

## 참고

| 문서 | 경로 |
|------|------|
| 테스트 플랜 | `test_plan.md` |
| 구현 대상 | `boundary/magic_square/boundary_validator.py`, `control/magic_square_control.py` |
| REFACTOR 계획 | `README.md` § REFACTOR 계획 |
