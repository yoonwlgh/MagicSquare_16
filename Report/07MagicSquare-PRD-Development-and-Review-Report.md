# Magic Square PRD Development and Review Report

## 1) 목적

Magic Square 4x4 TDD Practice 프로젝트의 **구현 전 PRD**를 작성하고,
7개 품질 기준으로 검토한 결과를 보고한다.

본 보고서는 다음 산출물의 맥락·범위·판정·후속 조치를 한곳에 정리한다.

- `docs/PRD_MagicSquare.md` (PRD 본문)
- PRD 작성 전 참고 문서 분석·매핑
- PRD 검토 결과 (수정 없이 문제·개선안만 기록)

## 2) 수행 범위

| 단계 | 내용 | 산출 |
|------|------|------|
| 1 | 참고 문서 분석 및 PRD 섹션 매핑 | 채팅 분석 결과 |
| 2 | PRD 본문 작성 (23개 섹션) | `docs/PRD_MagicSquare.md` |
| 3 | PRD 7기준 검토 | 본 보고서 §5 |

제외:

- PRD 본문 수정
- 구현 코드·테스트 코드
- RED 테스트 착수

## 3) 참고 문서 및 우선순위

| 논리명 | 저장소 경로 | PRD 반영 영역 |
|--------|-------------|---------------|
| Report/1 ProblemDefinition | `Report/01MagicSquare-Problem-Definition-Report.md` | Background, Why Chain, Invariant |
| Report/2 TDD Design | `Report/02MagicSquare-TDD-Design-Report.md` | Functional Contract, Domain Concept |
| Report/3 DevEnvironment/ECB | `Report/03MagicSquare-CursorRule-ECB-UserEntity-Implementation-Report.md` | Engineering Principles, NFR |
| Report/4 UserJourney | `Report/06MagicSquare-UserJourney-Story-Scenario-Report.md` | Epic, Journey, Story, Scenario |
| Cursor Rules | `.cursorrules`, `.cursor/rules/*.mdc` | Appendix, Quality Constraints |

**우선순위 규칙 (PRD 작성 시 적용):**

- 요구·검증: Report/4 우선
- 문제 정의·동기: Report/1 우선
- 기능 계약·불변식: Report/2 우선 + 사용자 고정 입출력 계약
- 품질·금지 규칙: Report/3, Cursor Rules 우선

## 4) PRD 산출물 요약

| 항목 | 값 |
|------|-----|
| **파일** | `docs/PRD_MagicSquare.md` |
| **문서 ID** | PRD-MS-4X4-001 |
| **버전** | 0.1.0-draft |
| **섹션** | §1 Executive Summary ~ §23 Appendix (23개) |
| **핵심 FR** | FR-01~FR-05 (Boundary 검증, Blank/Missing/Validator, Solver+Format) |
| **Business Rules** | BR-01~BR-14 |
| **Dual-Track** | Track A (Boundary Contract), Track B (Domain Invariant) |
| **Traceability** | §21 Matrix (Concept → BR → FR → AC → Test → Component) |

### 4.1 고정 입출력 계약 (PRD 반영)

**Input**

- 4×4 `int[][]`, `0` = 빈칸, 빈칸 정확히 2개
- 값: `0` 또는 `1~16`, 0 제외 중복 없음
- 첫 빈칸: row-major 최초 `0`

**Output**

- `int[6]`, 1-index, `[r1,c1,n1,r2,c2,n2]`
- Attempt 1: small→blank1, large→blank2
- Attempt 2: reverse 조합
- Both fail: `ERR_SOLVER_NO_SOLUTION` (Error Response)

## 5) PRD 검토 결과 (7기준)

> 검토 방식: PRD 본문 수정 없이 문제·개선안만 기록.

### 5.1 종합 판정

| # | 기준 | 판정 |
|---|------|------|
| 1 | 모든 FR에 테스트 가능 AC | **부분 충족** |
| 2 | 모든 AC ↔ Traceability Matrix | **미충족** (3개 AC 누락) |
| 3 | Boundary/Domain 책임 분리 | **부분 충족** |
| 4 | 오류 정책 미정 없음 | **부분 충족** |
| 5 | small-first / reverse 테스트 데이터 구분 | **미충족** |
| 6 | 1-index / row-major 규칙 | **부분 충족** |
| 7 | 구현·테스트 코드 미포함 | **충족** |

### 5.2 주요 문제 (우선순위)

| 우선순위 | ID | 문제 | 개선 방향 |
|----------|-----|------|-----------|
| P0 | P5-01~02 | TD-01 입력 행렬 PRD 미포함, TD-02/small-first 미확정 | §16.4에 입력·기대값 고정 |
| P0 | P2 | AC-FR02-01, AC-FR02-03, AC-FR03-03 Matrix 미연결 | §21 Matrix 보완 |
| P1 | P4-01 | EP-03 확정 vs DN-01 「Decision Needed」 모순 | DN-01 Closed 처리 |
| P1 | P3-01~05 | Control vs Domain Solver orchestration 경계 모호 | §17 Orchestration Sequence 추가 |
| P1 | P6-01~04 | row-major 알고리즘·두 번째 빈칸·1-index 변환식 미명시 | BR-06a, Coordinate Convention 절 |
| P2 | P1-01~02 | AC-FR02-01, AC-FR05-01 구체 Then 값 없음 | Given/Then 표 추가 |

### 5.3 Traceability Matrix 누락 AC

| AC ID | 내용 |
|-------|------|
| AC-FR02-01 | 빈칸 2개 좌표 정확 반환 |
| AC-FR02-03 | 0-index ↔ 1-index 변환 일치 |
| AC-FR03-03 | `0`은 누락 후보에서 제외 |

### 5.4 레이어 책임 이슈 요약

- §1·FR-01: 「Domain Solver 파이프라인」 표현 → Boundary가 Control 역할을 암시
- FR-05: Control(조율)·Domain(Solver)·Boundary(Format) 단일 FR → 레이어별 AC 분리 권장
- Solver Attempt 1→2 순서: Control 책임인지 Domain Solver 책임인지 API 수준 미정의

### 5.5 테스트 데이터 비대칭

| 케이스 | 입력 행렬 (PRD) | 기대 출력 (PRD) |
|--------|-----------------|-----------------|
| reverse (TD-01) | ❌ Report/4 참조만 | ✅ `[3,3,6,4,4,1]` |
| small-first (TD-02) | ❌ RED Phase defer | ❌ 형태만 (`n1=small, n2=large`) |

## 6) Open Questions (PRD §22 연계)

| ID | 상태 | 내용 |
|----|------|------|
| DN-01 | PRD stance (A) vs footnote 모순 | Error Response vs Exception — 검토 시 정리 필요 |
| DN-04 | **Decision Needed** | TD-02, TD-07 구체 행렬 RED Phase 확정 |
| DN-02 | Stance 기록됨 | Report/2 판정 계약 vs Solver PRD — Solver 우선 |

## 7) 생성/수정 파일

| 경로 | 설명 |
|------|------|
| `docs/PRD_MagicSquare.md` | PRD 본문 (v0.1.0-draft) |
| `Report/07MagicSquare-PRD-Development-and-Review-Report.md` | 본 보고서 |
| `Prompting/07cursor_magicsquare_prd_development_review_transcript.md` | 세션 Transcript Export |

## 8) 후속 권장

1. PRD v0.2: P0 이슈(TD-01/02 행렬, Matrix AC 3건) 반영
2. EP-03 / DN-01 모순 해소 후 Error Response Schema 고정
3. §17 Orchestration Sequence 및 FR-05 레이어 분리 검토
4. RED Phase 착수 전 TD-02/TD-07 행렬 확정
5. `Report/README.md`, 루트 `README.md`에 PRD·본 보고서 링크 추가

## 9) 결론

Magic Square 4x4 TDD Practice용 **구현 전 PRD**(`docs/PRD_MagicSquare.md`)를 작성·저장했고,
Dual-Track·입출력 계약·Traceability 골격은 갖추었으나,
**테스트 데이터 확정·AC-Matrix 완전 연결·Control/Domain orchestration·좌표 규칙 상세**에서 gap이 있다.

본 gap을 v0.2 PRD에서 보완한 뒤 RED Phase 착수하는 것을 권장한다.
