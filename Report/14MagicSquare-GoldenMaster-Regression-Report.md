# Magic Square Golden Master 회귀 안전장치 — 세션 보고서

## 1) 목적

Report/12(Dual-Track GREEN 62건·PyQt GUI) 이후, **Refactoring 전 회귀 보호**를 위해 Golden Master(Approval) 패턴을 도입하고 GM-1~GM-3 산출물을 기록한다.

본 보고서는 **REFACTOR 미착수**, **커버리지 게이트 미달성** 상태를 전제로 한다.

---

## 2) 수행 범위

| 단계 | ID | 내용 | 산출 | 상태 |
|------|-----|------|------|------|
| 1 | GM-1 | 기준 파일 생성 전략·approve 패턴 | `tests/golden_master_expected.txt`, `approval.py` | ✅ |
| 2 | GM-2 | GM-TC-01~05 테스트·계약 검증 | `test_golden_master_magic_square.py`, `contracts.py` | ✅ |
| 3 | GM-3 | docs/README Golden Master 섹션 | `docs/README.md` | ✅ |
| 4 | — | 생성 스크립트 | `scripts/generate_golden_master.py` | ✅ |
| 5 | — | pytest 마커 등록 | `pytest.ini` (`golden_master`) | ✅ |
| 6 | — | 설계 문서 | `docs/golden_master_approval_design.md` | ✅ |
| 7 | — | 루트 README 갱신 (80 passed, docs 링크) | `README.md` | ✅ |
| 8 | — | GitHub `stabilize/green` push | `b2407d7` | ✅ |
| 9 | — | Report·Transcript Export | 본 보고서, `Prompt/14` | ✅ |

**의도적 미수행:**

- GUI stdout Golden Master (DTO 계약만 GM-1~2 범위)
- syrupy / approvaltests 등 외부 snapshot 플러그인
- n×n 일반화

---

## 3) 참고 문서 및 추적

| 논리명 | 경로 | 본 세션 반영 |
|--------|------|--------------|
| PRD | `docs/PRD_MagicSquare.md` | §12 입출력 계약, Error Catalog |
| Report/12 | Dual-Track GREEN + PyQt | 62 passed 기준선 |
| test_plan.md | TP-MS-001 | TD-01~07 시나리오 |
| docs | `golden_master_approval_design.md` | approve 패턴 설계 |
| docs | `README.md` | GM-01~10 체크리스트 |

---

## 4) pytest 결과

### 4.1 세션 전후

| 시점 | passed | collected | golden_master |
|------|--------|-----------|---------------|
| Report/12 직후 | 62 | 62 | — |
| GM-1~2 추가 후 | **80** | **80** | **18** (`pytest -m golden_master`) |

### 4.2 Golden Master Test Case (GM-TC-01~05)

| TC ID | 시나리오 | 기대 | 검증 |
|-------|----------|------|------|
| GM-TC-01 | 정상 조합 (small-first) | `[3,2,6,3,3,7]` | int[6], 1-index, row-major, small-first |
| GM-TC-02 | reverse fallback | `[3,3,7,4,4,1]` | int[6], 1-index, row-major, reverse |
| GM-TC-03 | INVALID_BLANK_COUNT | `ERR_INVALID_BLANK_COUNT` | Boundary ErrorResponse |
| GM-TC-04 | DUPLICATE_NUMBER | `ERR_DUPLICATE_VALUE` | Boundary ErrorResponse |
| GM-TC-05 | NO_VALID_MAGIC_SQUARE | `ERR_SOLVER_NO_SOLUTION` | Control ErrorResponse |

**명령:**

```powershell
pytest -m golden_master -v
# → 18 passed, 62 deselected

python -m pytest tests/ -v
# → 80 passed
```

---

## 5) 구현 요약

### 5.1 Approve 패턴

| 동작 | 설명 |
|------|------|
| 기준 파일 없음 | 현재 솔버 출력으로 `golden_master_expected.txt` 자동 생성 |
| 기준 파일 있음 | `open(expected).read()` vs API 직렬화 결과 전체/섹션 비교 |
| 불일치 | `--- expected` / `+++ actual` unified diff 후 FAIL |
| 갱신 | `GOLDEN_MASTER_APPROVE=1` 또는 `python scripts/generate_golden_master.py` |

### 5.2 캡처 지점

```text
MagicSquareControl(BoundaryValidator(), MagicSquareDomainResolver()).solve(grid)
```

- **성공:** `list[int]` → `Output:` 블록
- **실패:** `ErrorResponse.code` → `Error:` 블록

### 5.3 신규·갱신 파일

| 경로 | 역할 |
|------|------|
| `tests/golden_master_expected.txt` | committed baseline (GM-TC-01~05) |
| `tests/golden_master/scenarios.py` | 5 시나리오 + `SolveStrategy` |
| `tests/golden_master/approval.py` | 직렬화, diff, approve |
| `tests/golden_master/contracts.py` | row-major, 1-index, 조합·Error 계약 |
| `tests/integration/test_golden_master_magic_square.py` | GM-2 메인 (`@pytest.mark.golden_master`) |
| `tests/integration/test_golden_master_solve.py` | GM-1 전체 문서 회귀 |
| `scripts/generate_golden_master.py` | baseline 생성 CLI |
| `pytest.ini` | `golden_master` 마커, `pythonpath=.` |
| `docs/README.md` | RED To-Do + Golden Master GM-01~10 |
| `docs/golden_master_approval_design.md` | GM-1/GM-2 설계 |

---

## 6) 기준 파일 구조 (발췌)

```text
[GM-TC-01]
Input:
16 3 2 13
...
Output:
[3, 2, 6, 3, 3, 7]
________________________________________
[GM-TC-03]
...
Error:
ERR_INVALID_BLANK_COUNT
```

---

## 7) Git 커밋 이력 (`stabilize/green`)

| 커밋 | 요약 |
|------|------|
| `b2407d7` | Add Golden Master regression suite (GM-1~3) with approve pattern and docs. |

**원격:** `https://github.com/yoonwlgh/MagicSquare_16.git` — branch `stabilize/green`

---

## 8) 검증 명령

```powershell
pytest -m golden_master -v
python scripts/generate_golden_master.py
python -m pytest tests/ -v
```

---

## 9) GM 체크리스트 (docs/README.md)

| 그룹 | ID | 상태 |
|------|-----|------|
| 기준 파일 | GM-01 ~ GM-03 | [x] |
| 테스트 코드 | GM-04 ~ GM-06 | [x] |
| 회귀 보호 | GM-07 ~ GM-10 | [x] |

---

## 10) 관련 산출물

| 유형 | 경로 |
|------|------|
| Transcript | `Prompt/14cursor_magicsquare_golden_master_transcript.md` |
| 설계 | `docs/golden_master_approval_design.md` |
| docs 인덱스 | `docs/README.md` |
| 이전 GREEN | `Report/12`, `Prompt/12` |

---

*문서 끝 — 작성 기준일: 2026-05-29 · 상태: Golden Master 18/18 · 전체 80/80 passed*
