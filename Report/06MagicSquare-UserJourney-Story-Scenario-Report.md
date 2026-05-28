# Magic Square User Journey/Story/Scenario Report

## 1) 목적

Magic Square 4x4 TDD Practice의 기획 흐름을
`Epic -> User Journey -> User Story -> Implementation Scenario` 관점으로 정리해,
다음 단계(Task 분해)에서 바로 사용할 수 있는 추적 가능한 기준선을 만든다.

## 2) 범위

- Level 1: Epic (Business Goal)
- Level 2: User Journey
- Level 3: User Stories + Acceptance Criteria
- Level 4: Implementation Scenario (Technical)

제외:
- 구현 코드
- 테스트 코드
- Task 수준 세분화

## 3) Level 1 Epic 요약

- Epic: `불변식 기반 사고 훈련 시스템 구축`
- 핵심 목표:
  - 불변식 중심 설계 사고
  - Dual-Track UI + Logic TDD 적용
  - 입력/출력 계약 명확화
  - 설계 -> 테스트 -> 구현 -> 리팩토링 흐름 정착
  - `Concept -> Invariant -> Contract -> Test` 추적성 확보
- 성공 기준:
  - Domain Logic 커버리지 95% 이상
  - Boundary 입력 검증 계약 테스트 100% 통과
  - 매직 넘버 금지 및 명명된 상수 사용
  - 정답 하드코딩 금지
  - 주요 Invariant별 테스트 추적 가능성 확보
  - 리팩토링 후 외부 입출력 계약 유지

## 4) Level 2 User Journey 요약

### Stage 1: Problem Recognition
- 과제를 "정답 구현"이 아닌 "불변식 검증 훈련"으로 재정의

### Stage 2: Contract Definition
- 입력/출력/오류 계약을 구현 전에 선명세

### Stage 3: Domain Separation
- 책임 분리 후보:
  - `BlankFinder`
  - `MissingNumberFinder`
  - `MagicSquareValidator`
  - `Solver`

### Stage 4: Dual-Track TDD Progress
- UI/Boundary RED와 Logic/Domain RED를 분리 운영
- GREEN 최소 변경 원칙과 REFACTOR 계약 보존 원칙 적용

### Stage 5: Regression Protection
- 정상/오류/조합 실패/출력 형식 케이스를 회귀 보호 대상으로 확장

## 5) Level 3 User Stories 요약

- Story 1 (Boundary): 입력 검증
  - 4x4 크기, 빈칸 2개, 값 범위, 0 제외 중복 규칙 위반 차단
  - 실패 시 Domain resolver 미호출

- Story 2 (Domain): 빈칸 좌표 탐색
  - 0 탐지, 2개 좌표 반환, row-major 순서, 좌표 기준 명시

- Story 3 (Domain): 누락 숫자 탐색
  - 0 제외, 1~16에서 누락 숫자 2개 계산, 오름차순 반환

- Story 4 (Domain): 마방진 검증
  - 행/열/대각선 합 34 동시 만족 시에만 유효 판정

- Story 5 (Control/Boundary Contract): 두 가지 조합 시도
  - small-first 실패 시 reverse 조합 재시도
  - 결과 `int[6]`, 1-index, `[r1,c1,n1,r2,c2,n2]` 형식 보장

## 6) Level 4 Implementation Scenario 요약

### SC-DOM-SOL-001
- small-first 조합 실패 후 reverse 조합 성공 시나리오
- 기대 반환값: `[3, 3, 6, 4, 4, 1]`
- 보호 Invariant:
  - 합 34 불변식
  - 1차 실패 시 reverse 재시도 불변식
- RED 후보: `RED-DOM-SOL-001`
- Task 후보: `TASK-DOM-SOL-001`

### SC-BND-VAL-001
- 빈칸 개수 오류(2개 아님) 입력 거부
- Domain 실행 차단
- RED 후보: `RED-BND-VAL-001`
- Task 후보: `TASK-BND-VAL-001`

### SC-BND-VAL-002
- 0 제외 중복 숫자 입력 거부
- Domain 실행 차단
- RED 후보: `RED-BND-VAL-002`
- Task 후보: `TASK-BND-VAL-002`

### SC-BND-VAL-003
- 값 범위 위반(0 또는 1~16 외 값) 입력 거부
- Domain 실행 차단
- RED 후보: `RED-BND-VAL-003`
- Task 후보: `TASK-BND-VAL-003`

## 7) 추적성 정리

- Epic Goal -> Journey Stage -> Story -> Scenario로 연계되어
  다음 단계에서 RED 테스트 ID 및 구현 Task ID를 분해할 수 있도록 준비됨.
- 특히 Story 1/5와 Scenario 묶음을 통해
  Boundary Contract 보호와 Solver 조합 시도 불변식을 명확히 추적 가능.

## 8) 다음 단계 권장

- Level 5에서 Story/Scenario 단위로 Task를
  `RED -> GREEN -> REFACTOR` 순서로 분해
- 각 Task에 `입력 계약`, `출력 계약`, `불변식` 연결 태그를 부여해
  회귀 보호 우선순위를 명시
