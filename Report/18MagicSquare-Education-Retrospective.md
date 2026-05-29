# Magic Square_JH — 교육 회고록

> **작성 근거:** [Report/01~17](./README.md) · [Prompt/01~16](../Prompt/) 세션 기록  
> **프로젝트:** 4×4 마방진 · ECB · TDD · Golden Master · REFACTOR (2026-05-28~29)

---

## 1. 교육에서 가장 도움이 된 내용

- **문제 재정의(Report/01, Prompt/01)** — 「34를 맞추는 퍼즐」이 아니라 **「제약을 만족하는지 판정하는 규칙을 테스트로 고정하는 것」**이 1차 목표라는 5 Whys 정리. 이후 PRD·테스트 플랜·AC가 한 방향으로 맞춰졌다.
- **Dual-Track TDD(Report/10~12, Prompt/10·12)** — Track A(Boundary FR-01)와 Track B(Domain FR-02~05)를 나눠 **FR-01 실패 시 `resolve()` 0회(BR-05)** 를 테스트로 증명하는 흐름이 가장 실무에 가깝게 느껴졌다.
- **RED → GREEN → REFACTOR 순서(Report/09→11→15→16)** — RED에서 `defect_list.md`로 실패를 근본 결함 5건으로 묶고, GREEN 후에만 REFACTOR를 열어도 **101 passed·GM 18건**을 유지할 수 있었다는 점.
- **ECB 레이어 규칙(Report/03, `.cursor/rules`)** — `boundary → control → entity` 의존 방향과 Control이 Boundary DTO에 직접 붙으면 안 된다는 제약이 Report/15 코드 리뷰·REFACTOR B그룹의 기준이 되었다.
- **Golden Master approve 패턴(Report/14, Prompt/14)** — `tests/golden_master_expected.txt` + diff + `GOLDEN_MASTER_APPROVE=1` 로 **리팩터 후에도 GM-TC-01~05 계약**을 자동으로 비교할 수 있게 된 점.

---

## 2. 처음 써 본 기능·워크플로

| 기능/워크플로 | 간단한 사용 경험 |
|---------------|------------------|
| **pytest + AAA + `@pytest.mark` 스켈레톤** | Report/10에서 21건을 `pytest.fail` 스켈레톤으로 모았다가, assert 활성화 후 Track별 GREEN(Report/12). |
| **`defect_list.md` 결함 추적** | Report/09 RED 24 fail을 DEF-001~005 근본 결함으로 매핑 → GREEN·REFACTOR 후 E-3에서 전건 CLOSE. |
| **HTML pytest 리포트** | `scripts/generate_test_report.ps1` · Prompt/11 — RED/GREEN 진행을 브라우저에서 공유·확인. |
| **PyQt6 데스크톱 GUI** | Report/12 — `python -m boundary.screen`으로 Validate/Solve·샘플 격자 로드; cov는 수동 스모크로 보완. |
| **Golden Master + approve** | Prompt/14 — 5 시나리오 baseline 생성·`pytest -m golden_master` 18건, 의도적 변경 시 approve로 baseline 갱신. |
| **Cursor Rule (`.cursor/rules/*.mdc`)** | Report/04 — ECB·TDD·Forbidden 규칙을 에이전트에 고정, REFACTOR 시 `print`/bare except 방지. |
| **GitHub PR · 브랜치 전략** | `feature/` → `stabilize/green` → PR #5 merge(Report/14), `refactor/refactor` → PR #6 → `develop` merge(Prompt/16). |
| **pytest-cov + fail-under 게이트** | Report/16 E-2 — `pytest.ini`에 FR-01/control 범위 85% gate; PyQt 제외와 전체 ECB 64%를 README에 분리 기록. |
| **Port/Adapter + ApplicationError** | Report/16 B그룹 — Control 전용 계약·`ValidationPort`로 Boundary import 제거. |
| **Report/Prompt 세션 Export** | 매 마일스톤마다 Report/0N + Prompt/0N transcript로 **무엇을 왜 했는지** 남기는 워크플로(Prompt/08·15·16). |

---

## 3. 막혔던 점과 해결 방법

| 어려움 | 어떻게 해결했는지 |
|--------|-------------------|
| AC-FR-01-01 RED **24건 전부 실패** — `validate()`가 항상 `None` (Report/09) | `defect_list.md`로 5개 근본 결함 정리 → `BoundaryValidator`에 형태·blank·range·duplicate 순 검증 GREEN(Report/11). |
| Dual-Track **collection ERROR** — `boundary.input_validator` 등 모듈 없음 (Report/10) | 패키지 경로 확정(`boundary/magic_square/`) 후 스켈레톤 21건 수집 가능하게 정리. |
| **OPEN-01** — test_plan `INVALID_SIZE` vs PRD `ERR_INVALID_SHAPE` (Report/15) | REFACTOR D-3에서 PRD 명칭·메시지로 통일, AC 28건·GM baseline diff 없음 유지. |
| REFACTOR **B-2** — resolver가 `ApplicationError`인데 GM/테스트는 `ErrorResponse` 기대 | `approval.py`·presenter·GM 테스트에 양쪽 DTO 허용 후, B-3에서 `ErrorResponse = ApplicationError` alias. |
| **Control → Boundary** import ECB 위반 (Report/15 C1) | `control/application_contracts.py`, `control/ports.py` 도입, `MagicSquareControl`은 Port만 의존(B-1). |
| REFACTOR 중 **회귀 불안** (80→93→101 증가) | Golden Master 18건 + REFACTOR 전 A그룹 unit test 추가(Report/15·16). |
| **`pytest -m golden_master`만 실행 시 cov 84%**로 gate 실패 (Report/16) | 게이트 범위에서 `boundary.cli` 제외·전체 스위트 기준 회귀 원칙을 README에 명시. |
| **PyQt UI cov 0%** — 전체 ECB 64%로 보임 | 커버리지 3단계(A 게이트 / B 마방진+entity / C 전체)로 나눠 오해 방지(Report/16·README). |
| README·defect_list의 **passed 수(80)와 실제(101) 불일치** | E-3 defect_list v0.2, Report/16, 회고 문서로 동기화. |

---

## 4. 팀 활동·페어 작업에서 배운 점

- 이 저장소는 **1인 개발 + AI 페어(Cursor Agent)** 가 주 흐름이었고, Prompt transcript에 사용자가 AC·브랜치·「RED만/GREEN만」처럼 **범위를 좁혀 주는 지시**를 반복한 패턴이 남아 있다. 범위가 클수록 한 번에 GREEN·REFACTOR를 섞지 않는 것이 안전하다는 걸 배웠다.
- **GitHub PR #3 코드 리뷰(Report/13, Prompt/13)** — 외부(또는 동료) 관점에서 ECB·테스트 갭을 짚어 주는 단계가 REFACTOR 계획(Report/15)으로 이어졌다. 리뷰는 「칭찬」보다 **아키텍처 위반·테스트 공백 목록**이 다음 스프린트 입력이 된다.
- **Report/Prompt 쌍으로 남기기** — 팀이 없어도 「다음 주의 나」 또는 리뷰어가 Report만 읽고 맥락을 복구할 수 있게 하는 **최소 협업 문서** 역할을 했다.
- (해당 시) 페어 프로그래밍을 했다면 여기에 **역할 분담·드라이버/네비게이터·합의한 AC 문구**를 추가하면 좋다.

---

## 5. 다음에 더 깊이 보고 싶은 주제

- **PyQt / headless UI 테스트** — `boundary.screen`을 cov·회귀에 넣는 방법(`pytest-qt` 등).
- **CI 파이프라인** — `develop` push 시 전체 pytest + golden_master + cov 범위 B를 job으로 분리.
- **Golden Master와 계약 변경** — OPEN-01처럼 code/message가 바뀔 때 approve·문서·AC를 한 번에 갱신하는 체크리스트 자동화.
- **Entity `MagicSquareValidator`** — 열·대각 실패 분기(현재 cov 80%)를 D-VAL 테스트로 채우기.
- **Port/Adapter 일반화** — User ECB 슬라이스와 마방진 슬라이스를 동일 패턴으로 묶는 방법.
- (교육 과정에서 다룬다면) **n×n 일반화** — 본 프로젝트는 의도적으로 4×4 고정(Report/01 scope).

---

## 6. 한 줄 요약

**「작은 마방진」을 통해 RED로 실패를 문서화하고, ECB·Golden Master·REFACTOR로 판정 규칙을 101개 테스트에 고정하는 법을 익혔다.**

---

*참고: [Report/17 — 프로젝트 회고 한 장](./17MagicSquare-Project-Retrospective-OnePage.md) · [Report/README.md](./README.md)*
