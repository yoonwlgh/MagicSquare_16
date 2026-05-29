# Magic Square_JH — 프로젝트 회고 (한 장 요약)

| 항목 | 내용 |
|------|------|
| **프로젝트** | 4×4 마방진 — 제약 판정·Solver·ECB 아키텍처 학습용 |
| **기간** | 2026-05-28 ~ 2026-05-29 (Report/01~16 기준) |
| **저장소** | [MagicSquare_16](https://github.com/yoonwlgh/MagicSquare_16.git) · 통합 브랜치 `develop` |
| **문서 근거** | [Report/01](./01MagicSquare-Problem-Definition-Report.md) ~ [Report/16](./16MagicSquare-REFACTOR-Execution-Report.md) |

---

## 한 줄 회고

「퍼즐 한 장을 맞추는 코드」가 아니라, **명시된 규칙을 테스트로 고정하고 ECB로 층을 나눈 뒤, Golden Master와 REFACTOR로 회귀·구조를 지킨 판정 시스템**을 만들었다.

---

## 여정 (Report 타임라인)

| 단계 | Report | 무엇을 했나 | pytest 등 |
|------|--------|-------------|-----------|
| **정의·설계** | 01~02, 06~07 | 5 Whys, Journey/Story, PRD 23섹션, TDD 2차 설계 | — |
| **기반** | 03~04, 08 | ECB User 슬라이스, Cursor Rule, AC-FR01-01 앵커 선정 | — |
| **RED** | 09~10 | 형태 검증 25건 RED, Dual-Track 21건 스켈레톤, defect 5건 | 24 fail → 결함 문서화 |
| **GREEN** | 11~12 | `BoundaryValidator` I-1, FR-01~05, Solver, PyQt GUI | **62 passed** |
| **안정화** | 13~14 | PR 리뷰, Golden Master GM-TC-01~05 approve | **80 passed** |
| **REFACTOR** | 15~16 | Port/Adapter, SRP, OPEN-01, cov gate, defect CLOSE | **101 passed** |

---

## 숫자로 보는 결과

| 지표 | 시작(RED) | 마감(develop) |
|------|-----------|----------------|
| pytest | 24 fail / 17 pass | **101 passed** |
| Golden Master | — | **18 passed** (baseline diff 0) |
| AC-FR-01-01 | 0 GREEN | **28 passed** |
| 결함 (defect_list) | OPEN 5 | **CLOSE 6** |
| cov CI 게이트 | 없음 | FR-01/control **100%** (129 stmts) |
| 산출 Report | — | **16본** + Prompt Export |

---

## 잘한 점 (Keep)

1. **문제 재정의(Report/01)** — 「34 맞추기」보다 **판정 규칙·불변식**을 1차 목표로 둔 덕에 TDD·테스트 플랜이 흔들리지 않았다.
2. **Dual-Track** — Boundary(Track A)와 Domain(Track B)을 나눠 FR-01 선행·Domain 격리(BR-05)를 테스트로 증명했다.
3. **RED→GREEN→REFACTOR 순서** — REFACTOR 전 Control unit test·GM 도입(Report/14~15)으로 리팩터 중 **80→101** 증가에도 GM 18건 유지.
4. **문서화 습관** — 세션마다 Report/Prompt Export로 **왜 그 시점에 무엇을 했는지** 추적 가능.
5. **ECB 정리(Report/16)** — Control→Boundary 역의존 제거, contracts SSOT, Presenter/Formatter 책임 분리.

---

## 아쉬웠던 점 · 극복 (Problem → Try)

| Problem | Try / 결과 |
|---------|------------|
| `INVALID_SIZE` vs PRD `ERR_INVALID_SHAPE` 혼재 (OPEN-01) | D-3에서 PRD 명칭 통일, AC 28건·GM 유지 |
| Control이 Boundary DTO에 직접 의존 (ECB 위반) | `application_contracts` + `ports` (B-1~B-3) |
| REFACTOR 시 회귀 불안 | Golden Master approve + cov `--cov-fail-under=85` |
| PyQt UI는 cov 0%에 가깝다 | 범위 A/B 게이트와 전체 ECB(64%) 분리 문서화 — **수동 스모크**로 보완 |
| defect_list·README·실제 pytest 수 불일치 | E-3·Report/16으로 **101 passed** 동기화 |

---

## 배운 점 (Learn)

- **작은 도메인(4×4)도** 계약(에러 code/message/layer)·격리·결정론은 테스트 설계 없이는 금방 깨진다.
- **「GREEN 많이」보다 「실패를 문서화한 RED」**가 이후 REFACTOR 속도를 만든다 (defect_list → CLOSE).
- **리팩터는 계획서(15)와 체크리스트(A~E) 없이** 하면 ECB·GM을 동시에 깨기 쉽다.
- **커버리지는 한 숫자가 아니다** — CI 게이트(마방진 트랙) vs PyQt 제외 전체 감사를 나눠야 오해가 없다.

---

## 최종 아키텍처·운영 (As-Is)

```text
boundary (FR-01 validate, FR-05 format, PyQt screen)
    → control (orchestrate, ApplicationError, SolverErrorMapper)
        → entity (BlankFinder, Solver, MagicSquareValidator)
```

- **검증:** `python -m pytest tests/` · `pytest -m golden_master`
- **수동:** `python -m boundary.screen`
- **기준선:** `tests/golden_master_expected.txt` (approve로 갱신)

---

## 남은 과제 (Next, 선택)

- PyQt `boundary.screen` headless 테스트 또는 cov `omit` 정책 확정  
- `entity.services` 열·대각 validator 분기 보강 (현재 80%)  
- `main` 브랜치 정리 · CI에서 cov 범위 B 별도 job  

---

## Report 색인 (전체 활동 맵)

| # | 주제 |
|---|------|
| 01 | 문제 정의 (5 Whys) |
| 02 | TDD 설계 |
| 03~04 | ECB User · Rule/Prompt |
| 05 | TODO Web 스택 (참고) |
| 06~07 | Journey · PRD |
| 08 | TDD 착수·README To-Do |
| 09~11 | AC-FR01-01 RED → GREEN |
| 10, 12 | Dual-Track RED → GREEN + PyQt |
| 13 | PR #3 코드 리뷰 |
| 14 | Golden Master |
| 15~16 | REFACTOR 계획 → 실행 |
| **17** | **본 회고 (한 장)** |

---

*2026-05-29 · MagicSquare_JH · develop 기준 · [Report/README.md](./README.md)*
