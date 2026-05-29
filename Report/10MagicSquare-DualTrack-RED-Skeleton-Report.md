# Magic Square Dual-Track RED Skeleton — 세션 보고서

## 1) 목적

Dual-Track UI + Logic TDD의 **RED(Skeleton)** 단계에서, Report/08·Report/09(AC-FR01-01 Full RED) 이후 **아직 pytest가 없던 Test ID**에 대해 테스트 스켈레톤만 작성하고, 수집·실행 결과를 기록한다.

본 보고서는 **GREEN/REFACTOR 미착수**, **운영 코드·stub 미작성** 상태를 전제로 한다.

---

## 2) 수행 범위

| 단계 | 내용 | 산출 | 상태 |
|------|------|------|------|
| 1 | SSOT 참조 (PRD, Report/02·06·08·09, `.cursorrules`) | 설계 추적 | ✅ |
| 2 | Track A 스켈레톤 U-IN-04~08, U-OUT-01~03, U-FLOW-02 | `tests/boundary/test_u_*.py` 3파일 | ✅ |
| 3 | Track B 스켈레톤 D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04 | `tests/entity/test_d_*.py` 4파일 | ✅ |
| 4 | G0~G3 픽스처 placeholder | `tests/conftest.py`, `tests/entity/conftest.py` | ✅ |
| 5 | pytest 실행·RED 확인 | collection ERROR 7 + 기존 스위트 유지 | ✅ |
| 6 | Report·Transcript Export | 본 보고서, `Prompt/10` | ✅ |

**의도적 미수행:**

- `boundary.input_validator`, `entity.services.*` 등 **production 구현**
- GREEN / REFACTOR
- Report/08 `test_ac_fr01_01_invalid_size.py` **수정·삭제**
- 실제 기대값 `assert` 작성

**중복 작성 금지 준수:**

- U-IN-01~03(형태/None/크기) → Report/08·09 `test_ac_fr01_01_invalid_size.py` 25건 Full RED에 포함

---

## 3) 참고 문서 및 추적

| 논리명 | 경로 | 본 세션 반영 |
|--------|------|--------------|
| PRD | `docs/PRD_MagicSquare.md` | FR-01~05, §12~13, §15 Dual-Track, AC-FR01-02~05, AC-FR02~05 |
| Report/02 | `Report/02MagicSquare-TDD-Design-Report.md` | I-1~I-10, 검사 순서 |
| Report/06 | `Report/06MagicSquare-UserJourney-Story-Scenario-Report.md` | SC-BND-VAL, SC-DOM-SOL-001 |
| Report/08 | `Report/08MagicSquare-TDD-Start-ToDo-README-Report.md` | U-IN-01~03 = AC-FR01-01 앵커 |
| Report/09 | `Report/09MagicSquare-AC-FR01-01-RED-Test-HTML-Report.md` | 25건 Full RED, defect_list |
| `.cursorrules` | 루트 | pytest, AAA, RED 선행, 80% 커버리지 |

> **Note:** 사용자 프롬프트의 `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md`·`Report/09 설계표`는 저장소에 별도 파일로 없음. Test ID 매핑은 **PRD §10~16 + Report/06 Scenario**로 정렬함.

---

## 4) RED Skeleton 규칙 (적용 요약)

| 규칙 | 적용 |
|------|------|
| 본문 | `pytest.fail("RED: <Test ID> — <한 줄 요약>")` 단일 라인 |
| AAA | Given/When/Then **주석만** |
| 명명 | `test_<test_id>_<scenario>` (예: `test_u_in_04_zero_empty_cells_returns_e002`) |
| import | `boundary.input_validator`, `entity.services.*` 등 **모듈 최상단** |
| Domain Mock | Track B **금지** |
| U-OUT / U-FLOW | Control mock/spy **주석**만 |
| D-SOL-02 | `pytest.fail("RED: D-SOL-02 — G2 TBD")` |
| G0~G3 | conftest **주석·placeholder** |

---

## 5) 생성 테스트 파일

### 5.1 Track A — Boundary (`tests/boundary/`)

| 파일 | Test ID | 건수 |
|------|---------|------|
| `test_u_in_input_validation.py` | U-IN-04 ~ U-IN-08 | 5 |
| `test_u_out_result_format.py` | U-OUT-01 ~ U-OUT-03 | 3 |
| `test_u_flow_domain_isolation.py` | U-FLOW-02 | 1 |

### 5.2 Track B — Entity (`tests/entity/`)

| 파일 | Test ID | 건수 |
|------|---------|------|
| `test_d_loc_blank_finder.py` | D-LOC-01 | 1 |
| `test_d_mis_missing_number_finder.py` | D-MIS-01 | 1 |
| `test_d_val_magic_square_validator.py` | D-VAL-01 ~ D-VAL-06 | 6 |
| `test_d_sol_solver.py` | D-SOL-01 ~ D-SOL-04 | 4 |

### 5.3 Fixture placeholder

| 파일 | 내용 |
|------|------|
| `tests/conftest.py` | G0~G3 주석 (G2 = TD-02 / D-SOL-02 TBD) |
| `tests/entity/conftest.py` | Entity 레이어 G1~G3 참조 주석 |

**신규 스켈레톤 합계:** **21 tests** (7 modules)

---

## 6) Test ID ↔ PRD 매핑표

| Test ID | 시나리오 요약 | PRD / AC | Error / 비고 |
|---------|---------------|----------|----------------|
| U-IN-04 | 빈칸 0개 | AC-FR01-02 | E002 → `ERR_INVALID_BLANK_COUNT` |
| U-IN-05 | 빈칸 1개 | AC-FR01-02 | E002 |
| U-IN-06 | 빈칸 3개 | AC-FR01-02 | E002 |
| U-IN-07 | 값 17 | AC-FR01-03 | E003 → `ERR_OUT_OF_RANGE` |
| U-IN-08 | 0 제외 중복 | AC-FR01-04 | E004 → `ERR_DUPLICATE_VALUE` |
| U-OUT-01 | `int[6]` 길이 6 | AC-FR05-04 | — |
| U-OUT-02 | 좌표 1-index | AC-FR05-05 | — |
| U-OUT-03 | reverse 성공 순서 | AC-FR05-02, TD-01 | `[3,3,6,4,4,1]` |
| U-FLOW-02 | 빈칸 오류 시 Domain 0회 | BR-05, EP-01 | U-FLOW-01(형태) 확장 |
| D-LOC-01 | BlankFinder row-major | AC-FR02-01/02 | — |
| D-MIS-01 | Missing `[small,large]` | AC-FR03-01/02 | — |
| D-VAL-01 | 행 합 34 | AC-FR04-01 | — |
| D-VAL-02 | 열 합 34 | AC-FR04-01 | — |
| D-VAL-03 | 주대각 34 | AC-FR04-01 | — |
| D-VAL-04 | 부대각 34 | AC-FR04-01 | — |
| D-VAL-05 | 완전 유효 → True | AC-FR04-01 | — |
| D-VAL-06 | 한 라인 불일치 → False | AC-FR04-02 | — |
| D-SOL-01 | reverse 성공 | AC-FR05-02 | SC-DOM-SOL-001 |
| D-SOL-02 | small-first 성공 | AC-FR05-01 | **G2 TBD** |
| D-SOL-03 | 두 조합 실패 | AC-FR05-03 | TD-07 TBD |
| D-SOL-04 | 입력 불변 | EP-04, NFR-04 | — |

---

## 7) pytest 실행 결과

**환경:** `.venv`, Python 3.14.0, pytest 9.0.3

**명령:**

```powershell
cd c:\DEV\MagicSquare_JH
.\.venv\Scripts\Activate.ps1
python -m pytest tests/boundary/ tests/entity/ -v --continue-on-collection-errors
```

| 구분 | 결과 |
|------|------|
| **신규 7 modules (21 Test ID)** | **7 collection ERROR** — `ModuleNotFoundError` (`boundary.input_validator`, `boundary.result_formatter`, `entity.services`) |
| **Report/08 AC-FR01-01** | 24 failed, 1 passed (변경 없음) |
| **User ECB 슬라이스** | 15 passed (`test_user*`, `test_user_cli_boundary`) |
| **판정** | 신규 스켈레톤 = **RED** (수집 단계 ERROR; 모듈 추가 후 `pytest.fail` FAILED 예상) |

**대표 collection ERROR:**

```text
ModuleNotFoundError: No module named 'boundary.input_validator'
ModuleNotFoundError: No module named 'boundary.result_formatter'
ModuleNotFoundError: No module named 'entity.services'
```

모듈 구현 후 동일 스켈레톤은 **FAILED** (`pytest.fail` 메시지)로 전환된다.

---

## 8) Dual-Track 분리 준수

| Track | 경로 | Mock |
|-------|------|------|
| A | `tests/boundary/test_u_*.py` | U-FLOW-02만 Control spy **주석** |
| B | `tests/entity/test_d_*.py` | Domain Mock **없음** |

**의존 방향 (목표):** `boundary → control → entity` — 스켈레톤 import 경로는 GREEN 시 ECB와 정합 필요.

---

## 9) OPEN 항목

| ID | 내용 | 비고 |
|----|------|------|
| OPEN-01 | `INVALID_SIZE` vs `ERR_INVALID_*` | Report/08·09 계승 |
| OPEN-02 | G2 / TD-02 small-first 행렬 | D-SOL-02 |
| OPEN-03 | TD-07 no-solution 행렬 | D-SOL-03 |
| OPEN-04 | `boundary.input_validator` vs `boundary.magic_square.boundary_validator` 통일 | GREEN 시 패키지 결정 |
| OPEN-05 | Report/09에 Dual-Track 설계표 문서화 | 본 세션 매핑표를 SSOT 후보로 사용 |

---

## 10) 생성·수정 파일 목록

| 경로 | 설명 |
|------|------|
| `tests/conftest.py` | G0~G3 placeholder |
| `tests/entity/conftest.py` | Entity fixture 주석 |
| `tests/boundary/test_u_in_input_validation.py` | U-IN-04~08 |
| `tests/boundary/test_u_out_result_format.py` | U-OUT-01~03 |
| `tests/boundary/test_u_flow_domain_isolation.py` | U-FLOW-02 |
| `tests/entity/test_d_loc_blank_finder.py` | D-LOC-01 |
| `tests/entity/test_d_mis_missing_number_finder.py` | D-MIS-01 |
| `tests/entity/test_d_val_magic_square_validator.py` | D-VAL-01~06 |
| `tests/entity/test_d_sol_solver.py` | D-SOL-01~04 |
| `Report/10MagicSquare-DualTrack-RED-Skeleton-Report.md` | 본 보고서 |
| `Prompt/10cursor_magicsquare_dual_track_red_skeleton_transcript.md` | Transcript |

**미수정 (의도):** `tests/boundary/test_ac_fr01_01_invalid_size.py`, `boundary/`, `control/` 마방진 GREEN 구현

---

## 11) 후속 권장 (GREEN 착수 순서)

1. OPEN-04: Boundary·Entity **모듈 경로** 확정 (`input_validator` vs `magic_square.boundary_validator`)
2. Track A: U-IN-04~08 GREEN — `InputValidator` / FR-01 빈칸·범위·중복
3. U-FLOW-02: Control + spy — BR-05 확장 회귀
4. Track B: D-LOC-01 → D-MIS-01 → D-VAL-01~06 → D-SOL-01 (G3) → D-SOL-02 (G2 확정 후)
5. U-OUT-01~03: `ResultFormatter` + FR-05 출력 계약
6. `pytest tests/boundary/test_u_*.py tests/entity/test_d_*.py` — 21건 `pytest.fail` → GREEN 전환
7. Report/09 defect_list·AC-FR01-01 25건과 회귀 통합 실행

---

## 12) 결론

Dual-Track **RED Skeleton 21건**이 `tests/boundary/test_u_*.py`·`tests/entity/test_d_*.py`에 추가되었으며, 미구현 모듈로 **7 collection ERROR**가 확인되었다. Report/08 AC-FR01-01 Full RED(25건)는 **변경 없이** 유지된다.

다음 공식 단계는 Boundary/Entity **최소 모듈 골격** 추가 후 스켈레톤을 `pytest.fail` FAILED로 수집하고, Test ID별 **GREEN 최소 구현**에 들어가는 것이다.
