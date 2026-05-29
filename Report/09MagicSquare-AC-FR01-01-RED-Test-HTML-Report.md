# Magic Square AC-FR01-01 RED 테스트 · HTML 리포트 세션 보고서

## 1) 목적

`test_plan.md` 및 README RED 체크리스트를 기준으로 **FR-01 / AC-FR01-01** 범위의 pytest RED 테스트를 작성·실행하고, 가상환경·HTML 테스트·커버리지 리포트 파이프라인을 구축한 결과를 기록한다.

본 보고서는 세션 종료 시점의 **산출물·실행 결과·RED 상태·후속 GREEN 항목**을 추적한다.

---

## 2) 수행 범위

| 단계 | 내용 | 산출 | 상태 |
|------|------|------|------|
| 1 | Report/ 기반 테스트 플랜 샘플 선정 (AC-FR01-01) | 선택 문서 (채팅) | ✅ |
| 2 | `test_plan.md` 작성 | TP-MS-001 v0.1 | ✅ |
| 3 | README `## RED 단계 To-Do 리스트` 삽입 | `README.md` 갱신 | ✅ |
| 4 | AC-FR01-01 RED pytest 25건 (5 카테고리 × 5) | `tests/boundary/test_ac_fr01_01_invalid_size.py` | ✅ |
| 5 | 계약·RED 스텁 (Boundary/Control) | `boundary/magic_square/*`, `control/magic_square_control.py` | ✅ RED 스텁 |
| 6 | `.venv` + `requirements-dev.txt` | venv, pydantic/pytest/pytest-cov/pytest-html | ✅ |
| 7 | HTML 테스트·커버리지 리포트 생성 | `report/pytest_report.html`, `htmlcov/` | ✅ |
| 8 | Report·Transcript Export | 본 보고서, `Prompt/09` | ✅ |
| 9 | 결함 목록 문서화 | `defect_list.md` (DEF-001~006) | ✅ |
| 10 | Report·Transcript defect_list 반영 | Report/09·Prompt/09 갱신 | ✅ |

**미수행 (의도적 — TDD GREEN 단계):**

- `BoundaryValidator.validate` GREEN 구현 (DEF-001~004)
- `MagicSquareControl.solve` Domain 격리 GREEN 구현 (DEF-005)
- README 「모든 결함 수정 후 회귀 테스트 통과」 체크

---

## 3) 참고 문서 및 추적

| 논리명 | 경로 | 본 세션 반영 |
|--------|------|--------------|
| PRD | `docs/PRD_MagicSquare.md` | FR-01, §12.1, §13.2, BR-05, EP-01 |
| 테스트 플랜 | `test_plan.md` | BV-001~006, RED-BND-001/ISO-001 |
| Report/02 | `Report/02MagicSquare-TDD-Design-Report.md` | S-011, I-1 선행 |
| Report/08 | `Report/08MagicSquare-TDD-Start-ToDo-README-Report.md` | 샘플 AC-FR01-01, OPEN-01 |
| README | `README.md` | RED To-Do (TC-A/B, 커버리지, defect_list 체크) |
| 결함 목록 | `defect_list.md` | DEF-001~005 Critical, DEF-006 Low, 24 fail → 5 root causes |

---

## 4) AC-FR01-01 앵커 계약

| 항목 | 값 |
|------|-----|
| **AC** | AC-FR01-01 (입력 형태 비성립) |
| **PRD** | FR-01, §12.1, §13.2, §16.2 ES-01 |
| **플랜 샘플 code** | `INVALID_SIZE` |
| **플랜 샘플 message** | `Grid must be 4x4.` |
| **PRD 공식 code** | `ERR_INVALID_SHAPE` (OPEN-01 미확정) |
| **Domain 호출** | No (BR-05, EP-01) |

---

## 5) RED 테스트 구성

### 5.1 파일

| 경로 | 역할 |
|------|------|
| `tests/boundary/test_ac_fr01_01_invalid_size.py` | RED 25 tests |
| `tests/boundary/conftest.py` | BoundaryValidator, Control, resolver spy |
| `boundary/magic_square/contracts.py` | `ErrorResponse`, 상수 (pydantic) |
| `boundary/magic_square/boundary_validator.py` | RED 스텁 (`validate` → `None`) |
| `control/magic_square_control.py` | RED 스텁 (실패 시에도 `resolve()` 호출) |

### 5.2 테스트 클래스 (각 5건)

| 클래스 | 검증 유형 |
|--------|-----------|
| `TestAcFr0101NormalFailureReturn` | `grid=None` → `INVALID_SIZE`, message, layer, `ErrorResponse` |
| `TestAcFr0101BoundaryValues` | `[]`, `[[]]*4`, 4×빈행, 3×4, 4×3 |
| `TestAcFr0101DomainIsolation` | `solve()` 후 `resolve.call_count == 0` |
| `TestAcFr0101MessageIdentity` | 메시지 문자·바이트 단위 동일 |
| `TestAcFr0101ScopeRestriction` | AC-FR01-02~04 코드 미반환, FR-02~05 테스트명 부재 |

### 5.3 형식 준수

- pytest, Given-When-Then 주석, `# AC-FR-01-01`
- 명명: `test_[입력조건]_[기대동작]_[검증포인트]`
- 클래스 docstring: `AC-FR-01-01, PRD §8.1 INVALID_SIZE` (세션 표기; PRD 본문 §8은 Journey, 계약 문구는 §12/플랜 샘플)

---

## 6) pytest 실행 결과 (최종 HTML 생성 시)

**환경:** `.venv` (Python 3.14.0), pytest 9.0.3, pytest-cov 7.1.0, pytest-html 4.2.0

| 구분 | 결과 |
|------|------|
| **수집** | 41 tests |
| **Passed** | 17 (User ECB 슬라이스 16 + scope 메타 1) |
| **Failed** | 24 (AC-FR01-01 RED — **의도된 RED**) |
| **판정** | RED 단계 확인 완료 |

**대표 실패 원인:**

- `BoundaryValidator.validate` → `None` (기대: `ErrorResponse`)
- `MagicSquareControl.solve(None)` → `resolve()` 호출됨 (기대: 0회)

---

## 7) 커버리지 (pytest-cov, htmlcov)

| 패키지 | Stmts | Miss | Cover |
|--------|-------|------|-------|
| boundary (magic_square + cli) | 23 | 0 | 100% |
| control (magic_square + user) | 19 | 1 | 94% |
| entity (user) | 30 | 0 | 100% |
| **TOTAL** | **72** | **1** | **99%** |

> 스텁만 존재하여 커버리지가 높게 나옴. GREEN 구현 후 **형태 검사 분기** 기준으로 재측정 필요. Boundary 85% / Domain 95% 게이트는 Track B 착수 후 별도 판정.

**미커버:** `control/magic_square_control.py` line 35 (`return validation_error` 분기 — 스텁이 항상 `None` 반환).

---

## 8) HTML 리포트 산출물

| 유형 | 경로 | 생성 명령 요약 |
|------|------|----------------|
| 테스트 결과 HTML | `report/pytest_report.html` | `--html=report/pytest_report.html --self-contained-html` |
| 커버리지 HTML | `htmlcov/index.html` | `--cov=boundary --cov=control --cov=entity --cov-report=html:htmlcov` |

**git 제외:** `.gitignore` — `htmlcov/`, `report/`, `.coverage` (기존 + `report/` 추가)

**의존성:** `requirements-dev.txt` — pytest, pytest-cov, pytest-html, pydantic

### 8.1 재실행 (참고)

```powershell
cd c:\DEV\MagicSquare_JH
.\.venv\Scripts\Activate.ps1
python -m pytest tests/ -v `
  --html=report/pytest_report.html `
  --self-contained-html `
  --cov=boundary --cov=control --cov=entity `
  --cov-report=html:htmlcov `
  --cov-report=term-missing
```

---

## 9) 개발 환경

| 항목 | 내용 |
|------|------|
| 가상환경 | `c:\DEV\MagicSquare_JH\.venv` |
| 생성 | `python -m venv .venv` |
| 활성화 | `.\.venv\Scripts\Activate.ps1` |
| 설치 | `pip install -r requirements-dev.txt` |

---

## 10) README RED To-Do 연동

`README.md`에 **## RED 단계 To-Do 리스트** 삽입 (기존 본문 유지):

- Track A: TC-A-01 ~ TC-A-07 — 미체크 (GREEN 대기)
- Track B: TC-B-01 ~ TC-B-04 — TC-B-04만 scope 메타 테스트로 통과
- 커버리지: Domain 95%+, Boundary 85%+, TOTAL 90%+ — 미체크
- 결함 목록 연결:
  - [x] `defect_list.md` 생성 및 발견 결함 기록 — [defect_list.md](../defect_list.md)
  - [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 11) 결함 목록 (`defect_list.md`)

**문서 ID:** DL-MS-001 v0.1 | **상태:** OPEN 5 / CLOSED 0 (Critical 5, Low 1)

pytest **24 failed** → 근본 결함 **5건**으로 집약 (영향 테스트 매핑은 `defect_list.md` §영향 테스트 매핑).

| ID | Severity | AC ID | 기대값 (요약) | 실제값 (요약) | 수정 요약 |
|----|----------|-------|---------------|---------------|-----------|
| **DEF-001** | Critical | AC-FR-01-01 | `grid=None` → `INVALID_SIZE` `ErrorResponse` | `None` | None·형태 비성립 분기 반환 |
| **DEF-002** | Critical | AC-FR-01-01 | `grid=[]` → `INVALID_SIZE` | `None` | 행 수 4×4 검사 |
| **DEF-003** | Critical | AC-FR-01-01 | `[[]]*4` → `INVALID_SIZE` | `None` | 열 길이 4 검사 |
| **DEF-004** | Critical | AC-FR-01-01 | 3×4·4×3 → `INVALID_SIZE` | `None` | `GRID_SIZE=4` 차원 검사 |
| **DEF-005** | Critical | AC-FR-01-01, BR-05 | `resolve()` 0회 | `call_count >= 1` | 검증 실패 시 resolve 금지 |
| **DEF-006** | Low | AC-FR-01-01 | Control line 35 커버 | Miss | DEF-001~005 수정 시 해소 예상 |

**GREEN 우선순위:** DEF-001 → DEF-002~004 (통합 validate) → DEF-005 → 회귀·DEF-006 확인.

**CLOSE 조건:** `test_ac_fr01_01_invalid_size.py` 25 passed, 전체 41 passed, README 회귀 체크박스 완료.

---

## 12) OPEN 항목

| ID | 내용 | 비고 |
|----|------|------|
| OPEN-01 | `INVALID_SIZE` vs `ERR_INVALID_SHAPE` | Report/08 계승; GREEN 시 상수 통일 |
| OPEN-02 | PRD §8.1 vs §12.1 섹션 표기 통일 | 테스트 docstring·README |
| ~~OPEN-03~~ | ~~`defect_list.md` 미생성~~ | **해소** — DL-MS-001 작성 완료 |
| OPEN-04 | GREEN: `BoundaryValidator` None/형태 분기 | DEF-001~004, RED-BND-001 |
| OPEN-05 | GREEN: `MagicSquareControl` 검증 실패 시 resolve 미호출 | DEF-005, RED-BND-ISO-001 |
| OPEN-06 | 결함 CLOSE 및 README 회귀 체크 | DEF-001~005 수정 후 |

---

## 13) 생성·수정 파일 목록

| 경로 | 설명 |
|------|------|
| `test_plan.md` | AC-FR01-01 테스트 계획서 |
| `tests/boundary/test_ac_fr01_01_invalid_size.py` | RED 25 tests |
| `tests/boundary/conftest.py` | 픽스처 |
| `boundary/magic_square/contracts.py` | pydantic 계약 |
| `boundary/magic_square/boundary_validator.py` | RED 스텁 |
| `control/magic_square_control.py` | RED 스텁 |
| `requirements-dev.txt` | dev 의존성 |
| `README.md` | RED To-Do + defect_list 링크·체크 |
| `defect_list.md` | 결함 DL-MS-001 (DEF-001~006) |
| `.gitignore` | `report/` 추가 |
| `report/pytest_report.html` | HTML 테스트 리포트 (생성물) |
| `htmlcov/` | HTML 커버리지 (생성물) |
| `Report/09MagicSquare-AC-FR01-01-RED-Test-HTML-Report.md` | 본 보고서 |
| `Prompt/09cursor_magicsquare_ac_fr01_01_red_html_transcript.md` | Transcript |

---

## 14) 후속 권장 (GREEN)

1. OPEN-01 에러 코드·메시지 단일 상수 확정  
2. `defect_list.md` DEF-001~004 순으로 `BoundaryValidator.validate` 구현  
3. DEF-005: `MagicSquareControl.solve` — 검증 실패 시 `resolve()` 호출 금지  
4. `pytest tests/boundary/test_ac_fr01_01_invalid_size.py` → 25 passed  
5. `defect_list.md` DEF-001~005 **CLOSED**, OPEN-06 README 회귀 체크  
6. README RED To-Do TC-A/B 체크, HTML 리포트 재생성  

---

## 15) 결론

Magic Square 프로젝트는 **AC-FR01-01 RED 테스트 25건·가상환경·HTML 리포트·결함 목록(`defect_list.md`)** 까지 완료되었으며, pytest **24 failed / 17 passed**는 **의도된 RED 상태**이다.

근본 결함 **5건(DEF-001~005)** 이 GREEN 범위를 정의한다. 다음 공식 단계는 결함표 수정 요약대로 **Boundary 검증 + Control 격리** 구현 후 회귀·결함 CLOSE이다.
