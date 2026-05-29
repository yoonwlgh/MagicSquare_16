# MagicSquare 문서 인덱스

구현·테스트 기준 문서 모음입니다.

| 문서 | 설명 |
|------|------|
| [PRD_MagicSquare.md](./PRD_MagicSquare.md) | 4×4 마방진 PRD (FR-01~FR-05, 입출력 계약) |
| [golden_master_approval_design.md](./golden_master_approval_design.md) | Golden Master approve 패턴 설계 (GM-1, GM-2) |

---

## RED 단계 To-Do 리스트

> 상세 TDD 체크리스트: [README.md § TDD 진행 체크리스트](../README.md#tdd-진행-체크리스트)  
> 표기: `[ ]` 미완 · `[x]` 완료

| 상태 | 항목 | 비고 |
|------|------|------|
| [x] | AC-FR-01-01 RED → GREEN (25건) | `test_ac_fr01_01_invalid_size.py` |
| [x] | Track A U-IN / U-FLOW / U-OUT GREEN | Boundary 입력·출력 계약 |
| [x] | Track B D-LOC ~ D-SOL GREEN | Domain 불변식·Solver |
| [ ] | TC-BND-006 (5×5), DET-001, IMM-001 | 미작성 |
| [ ] | 커버리지 게이트 (Domain 95%+, Boundary 85%+, TOTAL 90%+) | `pytest-cov` |

---

## Golden Master 회귀 안전장치

Refactoring 시작 전 구축.  
GREEN 완료 후 즉시 적용.

### 기준 파일 생성

| 상태 | ID | 내용 |
|------|-----|------|
| [x] | GM-01 | `tests/golden_master_expected.txt` 생성 |
| [x] | GM-02 | 정상 / reverse / 오류 시나리오 추가 (GM-TC-01~05) |
| [x] | GM-03 | `git add tests/golden_master_expected.txt` (버전 관리 포함) |

```powershell
python scripts/generate_golden_master.py
git add tests/golden_master_expected.txt
```

### 테스트 코드

| 상태 | ID | 내용 |
|------|-----|------|
| [x] | GM-04 | `tests/integration/test_golden_master_magic_square.py` 작성 |
| [x] | GM-05 | approve 패턴 적용 (`tests/golden_master/approval.py`) |
| [x] | GM-06 | Golden Master 테스트 PASS 확인 |

```powershell
pytest -m golden_master -v
```

### 회귀 보호

| 상태 | ID | 보호 대상 | 검증 위치 |
|------|-----|-----------|-----------|
| [x] | GM-07 | row-major 규칙 | `tests/golden_master/contracts.py` |
| [x] | GM-08 | 1-index 출력 | `tests/golden_master/contracts.py` |
| [x] | GM-09 | reverse 조합 fallback | `tests/golden_master/contracts.py` |
| [x] | GM-10 | Error Contract | `tests/golden_master/contracts.py` |

**관련 파일**

```text
tests/golden_master_expected.txt          # committed baseline
tests/golden_master/                      # scenarios, approval, contracts
tests/integration/test_golden_master_magic_square.py
scripts/generate_golden_master.py
pytest.ini                                # marker: golden_master
```

**실행 예시 (18 passed)**

```text
$ pytest -m golden_master -v
tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_golden_master_section_matches_baseline[normal_success] PASSED
...
====================== 18 passed, 62 deselected =======================
```

---

*문서 버전: GM-3 / MagicSquare_JH*
