# Magic Square REFACTOR 계획 — 세션 보고서

## 1) 목적

Report/14(Golden Master GM-1~3, 80 passed) 이후, **REFACTOR phase 착수 전** 코드 리뷰·SRP 점검·테스트 갭 분석 결과를 **리팩토링 계획서**로 고정한다.

본 문서는 **구현·리팩터 미착수** 상태의 계획 기록이다.

---

## 2) 수행 범위 (본 세션)

| 단계 | 내용 | 산출 | 상태 |
|------|------|------|------|
| 1 | 전체 코드 리뷰 (ECB, GM, 테스트 갭) | code-reviewer 분석 | ✅ |
| 2 | control/boundary SRP 점검 (함수·클래스·UI) | 위반 목록 | ✅ |
| 3 | REFACTOR 계획서 작성 (우선순위·테스트 선행·검증) | `README.md` § REFACTOR 계획 | ✅ |
| 4 | Report·Transcript Export | 본 보고서, `Prompt/15` | ✅ |

**의도적 미수행:**

- Port/Adapter 구현
- Control unit test 추가
- 실제 REFACTOR 커밋 (코드 구조 변경)

---

## 3) 참고 문서

| 논리명 | 경로 | 본 세션 반영 |
|--------|------|--------------|
| Report/14 | Golden Master GM-1~3 | 80 passed baseline |
| docs | `golden_master_approval_design.md`, `docs/README.md` | GM 회귀 안전장치 |
| 규칙 | `.cursorrules` refactor_phase | 외부 동작 불변·cov 80% |
| test_plan | TC-BND-006, DET-001, IMM-001 | 미작성 RED |

---

## 4) pytest baseline

| 항목 | 값 |
|------|-----|
| 전체 | **80 / 80 passed** |
| Golden Master | **18 / 18** (`pytest -m golden_master`) |
| RED 스켈레톤 (`pytest.fail`) | **0건** |

---

## 5) 코드 리뷰 핵심 (요약)

| ID | 심각도 | 내용 |
|----|--------|------|
| C1 | Critical | Control→Boundary import (ECB 위반) |
| C2 | Critical | AC-FR04-03 / BR-11 `MagicSquareValidator` 미구현 |
| C3 | Critical | OPEN-01: `INVALID_SIZE` vs `ERR_INVALID_SHAPE` |
| M1 | Major | U-FLOW range/duplicate Domain 격리 미검증 |
| M4 | Major | `tests/control/test_magic_square_*.py` 없음 |

---

## 6) SRP 점검 요약 (control/ · boundary/)

### ① 함수 다중 역할 (위반)

| 파일:줄 | 역할 1 | 역할 2 |
|---------|--------|--------|
| `boundary/result_formatter.py:11` | 출력 계약 검증 | int[6] 정규화·반환 |
| `control/magic_square_resolver.py:22` | Solver 호출 | ErrorResponse 조립 |
| `boundary/cli/user_cli_boundary.py:21` | payload 파싱·Control 호출 | dict 직렬화 |
| `boundary/screen/main_window.py:37` | Presenter 주입 | UI 구성 트리거 |
| `boundary/screen/main_window.py:47` | UI 레이아웃 | 샘플 데이터 wiring |

### ② 클래스 — 데이터+검증 혼재

**해당 없음**

**클래스 복수 책임:** `boundary/screen/presenter.py:12` — use-case 위임 + 출력 포맷

### ③ main_window UI 비즈니스 판단

**해당 없음** (Presenter 위임·DTO→문자열만)

---

## 7) 리팩토링 대상 (우선순위)

| 순번 | 대상 | 문제 | 기법 | 우선순위 |
|------|------|------|------|----------|
| 1 | control + contracts | Control→Boundary ECB 위반 | Port/Adapter | P0 |
| 2 | tests/control (신규) | Control unit test 없음 | RED→GREEN 선행 | P0 |
| 3 | U-FLOW, boundary_validator | blank만 격리; BND-006/DET/IMM 미작성 | 테스트 보강 | P0 |
| 4 | magic_square_resolver | Solver + ErrorResponse 이중 역할 | ErrorMapper 추출 | P1 |
| 5 | result_formatter | 검증 + 포맷 | Validator 분리 | P1 |
| 6 | presenter | use-case + format 복수 책임 | ViewFormatter 추출 | P1 |
| 7 | main_window | DI + UI 혼재 | Composition Root | P2 |
| 8 | user_cli_boundary | 파싱 + 직렬화 | Extract Method | P2 |
| 9 | input_validator / boundary_validator | Facade 중복 (OPEN-04) | 단일 진입점 | P2 |
| 10 | constants / contracts | 상수 이중 정의 | entity SSOT | P2 |
| 11 | contracts | OPEN-01 코드명 | Rename + GM 재approve | P2 |
| 12 | test_u_out | Entity 직접 호출 | Control E2E 정렬 | P2 |
| 13 | defect_list.md | 80 passed와 불일치 | 문서 동기화 | P3 |

상세: [README.md § REFACTOR 계획](../README.md#refactor-계획)

---

## 8) 테스트 선행 (REFACTOR 전 RED→GREEN)

| 대상 | 테스트 파일 | 검증 |
|------|-------------|------|
| `MagicSquareControl.solve()` | `tests/control/test_magic_square_control.py` (신규) | validate 실패 → resolver 0회 |
| `MagicSquareDomainResolver.resolve()` | `tests/control/test_magic_square_resolver.py` (신규) | `SolverNoSolutionError` → Control layer |
| `BoundaryValidator.validate()` | `test_ac_fr01_01_invalid_size.py` | TC-BND-006, DET-001, IMM-001 |
| U-FLOW range/duplicate | `test_u_flow_domain_isolation.py` | resolver spy 0회 |
| `ResultFormatter.to_int6()` | `test_u_out_result_format.py` | negative → ValueError |
| Presenter (선택) | `test_screen_presenter.py` (신규) | validate/solve/format_* |

---

## 9) REFACTOR 후 검증

```powershell
python -m pytest tests/ -v
pytest -m golden_master -v
python -m pytest tests/ --cov=boundary --cov=control --cov=entity --cov-report=term-missing
python scripts/generate_golden_master.py
git diff tests/golden_master_expected.txt
python -m boundary.screen
```

---

## 10) 관련 산출물

| 유형 | 경로 |
|------|------|
| Transcript | `Prompt/15cursor_magicsquare_refactor_plan_transcript.md` |
| REFACTOR 계획 (README) | `README.md` § REFACTOR 계획 |
| Golden Master | Report/14, Prompt/14 |

---

*문서 끝 — 작성 기준일: 2026-05-29 · 상태: REFACTOR 계획 수립 · 구현 미착수*
