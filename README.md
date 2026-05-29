# MagicSquare_JH

4×4 **마방진(Magic Square)** 을 다루는 TDD 훈련 프로젝트입니다.

겉으로는 「행·열·대각선 합이 34가 되는 4×4 격자를 만든다」는 과제이지만, 이 저장소의 **진짜 목표**는 다음과 같습니다.

> **4×4 정수 격자가 명시된 제약을 만족하는지 판정하는 규칙을 정의하고, 그 판정을 반복 가능하게 적용하며, 기준을 테스트로 고정·회귀할 수 있게 하는 것**

유효한 격자 **하나를 산출**하는 Solver는, 위 판정 규칙이 확립된 뒤의 **2차 목표**로 둡니다.

---

## 현재 상태

| 단계 | 항목 | 상태 | 산출물 |
|------|------|------|--------|
| 1 | 문제 정의 (STEP 1~5) | ✅ 완료 | [Report/01](./Report/01MagicSquare-Problem-Definition-Report.md) |
| 2 | TDD 설계 (판정 1차, 생성 2차) | ✅ 완료 | [Report/02](./Report/02MagicSquare-TDD-Design-Report.md) |
| 3 | Cursor Rule + ECB User 수직 슬라이스 | ✅ 완료 | [Report/03](./Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md) |
| 4 | 규칙 분할 + Prompt 경로 통일 | ✅ 완료 | [Report/04](./Report/04MagicSquare-Rule-Expansion-and-Prompt-Export-Report.md) |
| 5 | TODO Web 기술 스택 검토 | ✅ 완료 | [Report/05](./Report/05TodoWeb-Stack-Recommendation-Report.md) |
| 6 | User Journey / Story / Scenario | ✅ 완료 | [Report/06](./Report/06MagicSquare-UserJourney-Story-Scenario-Report.md) |
| 7 | PRD 작성 + 7기준 검토 | ✅ 완료 | [Report/07](./Report/07MagicSquare-PRD-Development-and-Review-Report.md), [docs/PRD](./docs/PRD_MagicSquare.md) |
| 8 | 마방진 도메인 구현 (Solver/Validator) | ⏳ 미착수 | PRD FR-01~FR-05 기준 RED 테스트 대기 |

**코드 현황:** ECB 아키텍처 검증용 `User` 수직 슬라이스 구현 완료 — **16 tests passed** (pytest).  
**마방진 Solver/Validator 본 구현은 PRD 기준으로 아직 착수 전입니다.**

---

## 진행 타임라인

```text
STEP 1~5 문제 정의
    → TDD 설계 (불변식 I-1~I-10, P0 시나리오)
    → ECB + Cursor Rule + User 수직 슬라이스 (개발 환경 정착)
    → 규칙 .mdc 분할 + Prompt/Report 체계화
    → Epic → Journey → Story → Scenario 기획
    → PRD v0.1.0-draft + 7기준 검토
    → [다음] Dual-Track TDD로 마방진 도메인 RED 착수
```

---

## 문제 정의 요약

### 표면 정의 vs 정확한 정의

| 구분 | 내용 |
|------|------|
| **표면 (피해야 할 정의)** | 1~16을 넣어 행·열·대각 합이 모두 34인 배치를 **만든다** |
| **정확한 정의** | 제약(크기, 범위, 중복 없음, 선별 합 동일)을 **판정**하고, 그 규칙을 **고정·검증**한다 |

### 핵심 불변 조건 (Invariant)

4×4, 값 **1~16** 각 **한 번**, **마법 상수 34**:

- **I-1 ~ I-3:** 4×4 형태, 범위, 중복 없음
- **I-4 ~ I-7:** 각 행·열·주대각·부대각선 합 = 34
- **I-8 ~ I-10:** 전부 만족 시에만 유효, 동일 입력 → 동일 판정, 규칙 변경은 계약(테스트) 변경

상세: [Report/01 — 문제 정의 통합 보고서](./Report/01MagicSquare-Problem-Definition-Report.md)

---

## PRD 요약 (구현 전 기준)

| 항목 | 내용 |
|------|------|
| 문서 | [docs/PRD_MagicSquare.md](./docs/PRD_MagicSquare.md) |
| ID / 버전 | PRD-MS-4X4-001 / 0.1.0-draft |
| 핵심 FR | FR-01~FR-05 (Boundary 검증, Blank/Missing/Validator, Solver+Format) |
| Business Rules | BR-01~BR-14 |
| TDD 전략 | Dual-Track — Track A (Boundary Contract), Track B (Domain Invariant) |

### 고정 입출력 계약

**Input**

- 4×4 `int[][]`, `0` = 빈칸, 빈칸 정확히 2개
- 값: `0` 또는 `1~16`, 0 제외 중복 없음
- 첫 빈칸: row-major 최초 `0`

**Output**

- `int[6]`, 1-index, `[r1,c1,n1,r2,c2,n2]`
- Attempt 1: small→blank1, large→blank2
- Attempt 2: reverse 조합
- Both fail: `ERR_SOLVER_NO_SOLUTION`

PRD 7기준 검토 결과(부분 충족 항목·개선안): [Report/07 §5](./Report/07MagicSquare-PRD-Development-and-Review-Report.md)

---

## 아키텍처

### ECB 레이어

| 레이어 | 책임 | 예시 |
|--------|------|------|
| `boundary/` | 외부 I/O, 파싱·직렬화 | CLI, API adapter |
| `control/` | 유스케이스 조율 | Solver 파이프라인 순서 |
| `entity/` | 순수 도메인 규칙 | Validator, BlankFinder, Solver |

**의존 방향:** `boundary → control → entity` (역방향 금지)

### Dual-Track TDD

| Track | 대상 | RED 예시 |
|-------|------|----------|
| Track A | Boundary 입력/출력 계약 | 빈칸 개수 오류, 중복·범위 위반 거부 |
| Track B | Domain 불변식 | BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver |

---

## 저장소 구조

```text
MagicSquare_JH/
├── README.md                          # 이 파일
├── .cursorrules                       # 프로젝트 규칙 요약
├── .cursor/
│   ├── rules/                         # 주제별 Cursor Rule (.mdc)
│   └── agents/                        # code-reviewer, ux-design-advisor
├── boundary/                          # ECB — 외부 I/O
│   └── cli/user_cli_boundary.py
├── control/                           # ECB — 유스케이스 조율
│   └── user_control.py
├── entity/                            # ECB — 도메인 규칙
│   └── user.py
├── tests/                             # 레이어별 pytest (AAA)
│   ├── boundary/test_user_cli_boundary.py
│   ├── control/test_user_control.py
│   └── entity/test_user.py
├── docs/
│   └── PRD_MagicSquare.md             # 구현 전 PRD (23개 섹션)
├── Report/                            # 단계별 보고서
│   ├── README.md
│   ├── 01MagicSquare-Problem-Definition-Report.md
│   ├── 02MagicSquare-TDD-Design-Report.md
│   ├── 03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md
│   ├── 04MagicSquare-Rule-Expansion-and-Prompt-Export-Report.md
│   ├── 05TodoWeb-Stack-Recommendation-Report.md
│   ├── 06MagicSquare-UserJourney-Story-Scenario-Report.md
│   └── 07MagicSquare-PRD-Development-and-Review-Report.md
└── Prompt/                            # Cursor 대화·프롬프트 기록
    ├── 01cursor_4x4_magic_square_problem_definit.md
    ├── 02cursor_magicsquare_tdd_prompt_transcript.md
    ├── 03cursor_magicsquare_rule_ecb_transcript.md
    ├── 04cursor_magicsquare_rule_expansion_transcript.md
    ├── 05todo_web_stack_recommendation_transcript.md
    └── 06cursor_magicsquare_user_journey_story_scenario_transcript.md
```

---

## 개발 환경 및 테스트

### 요구 사항

- Python 3.10+
- pytest

### 테스트 실행

```bash
python -m pytest tests/ -v
```

현재 ECB 검증용 User 슬라이스: **16 passed**

### Cursor Rule (.cursor/rules/)

| 파일 | 내용 |
|------|------|
| `magicsquare-project.mdc` | 프로젝트 범위, 마방진 도메인 목표 |
| `magicsquare-ecb-architecture.mdc` | ECB 레이어 책임·의존 방향 |
| `magicsquare-tdd-testing.mdc` | Dual-Track TDD, pytest, AAA, 80% 커버리지 |
| `magicsquare-python-code-style.mdc` | PEP8, 타입 힌트, Google docstring |
| `magicsquare-forbidden.mdc` | print 금지, bare except 금지, RED 선행 등 |

---

## User Story 요약 (Report/06)

| Story | 레이어 | 내용 |
|-------|--------|------|
| 1 | Boundary | 4×4, 빈칸 2개, 값 범위, 0 제외 중복 검증 — 실패 시 Domain 미호출 |
| 2 | Domain | `BlankFinder` — 0 탐지, 2개 좌표, row-major 순서 |
| 3 | Domain | `MissingNumberFinder` — 1~16 누락 2개, 오름차순 |
| 4 | Domain | `MagicSquareValidator` — 행/열/대각 합 34 동시 만족 |
| 5 | Control/Boundary | Solver — small-first 실패 시 reverse, `int[6]` 형식 보장 |

---

## 범위

### In scope

- 4×4 정수 격자 유효성 **판정** 규칙 (I-1 ~ I-10)
- 빈칸 2개 Solver 입출력 계약 (PRD §12)
- ECB 분리, Dual-Track TDD, pytest 회귀 보호
- 판정·Solver 규칙의 반복 가능성·테스트 고정

### Out of scope (현 단계)

- UI / Web / DB
- n×n 일반화, 모든 해 나열
- TODO Web 실제 구현 (Report/05는 기술 스택 **검토**만)

---

## 다음 단계

1. PRD 검토 P0 이슈 반영 (테스트 데이터 TD-01/TD-02, Traceability Matrix 보완)
2. Story/Scenario 단위 **RED** 테스트 작성 (Boundary → Domain 순)
3. Dual-Track TDD: Track A(Boundary Contract) + Track B(Domain Invariant)
4. `BlankFinder` → `MissingNumberFinder` → `MagicSquareValidator` → `Solver` 순 구현
5. Domain Logic 커버리지 95%+, Boundary 계약 테스트 100% 목표 (Epic 성공 기준)

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록 — [defect_list.md](./defect_list.md) (DEF-001~006, 24 failed → 5 root causes)
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 문서 인덱스

| 문서 | 설명 | 작성일 |
|------|------|--------|
| [Report/01 — 문제 정의](./Report/01MagicSquare-Problem-Definition-Report.md) | STEP 1~5 통합 (Invariant I-1~I-10) | 2026-05-28 |
| [Report/02 — TDD 설계](./Report/02MagicSquare-TDD-Design-Report.md) | 판정 1차·생성 2차, P0 시나리오 | 2026-05-28 |
| [Report/03 — ECB User 구현](./Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md) | Cursor Rule + User 수직 슬라이스 | 2026-05-28 |
| [Report/04 — 규칙 확장](./Report/04MagicSquare-Rule-Expansion-and-Prompt-Export-Report.md) | .mdc 분할, Prompt 경로 통일 | 2026-05-28 |
| [Report/05 — TODO Web 스택](./Report/05TodoWeb-Stack-Recommendation-Report.md) | React+TS+Vite 권장 (참고용) | 2026-05-28 |
| [Report/06 — Journey/Story/Scenario](./Report/06MagicSquare-UserJourney-Story-Scenario-Report.md) | Epic~Level 4 시나리오 | 2026-05-28 |
| [Report/07 — PRD 작성·검토](./Report/07MagicSquare-PRD-Development-and-Review-Report.md) | PRD 산출 + 7기준 검토 | 2026-05-29 |
| [docs/PRD_MagicSquare.md](./docs/PRD_MagicSquare.md) | 구현 전 PRD 본문 (23개 섹션) | 2026-05-29 |
| [Report/README.md](./Report/README.md) | Report 폴더 목차 | — |

---

## 라이선스

미정 (추가 예정)
