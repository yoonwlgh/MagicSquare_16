# Magic Square TDD Start — To-Do · README Transcript (Export)

_Export scope: 테스트 플랜 샘플 선정 → 통합 To-Do → Dual-Track 추적 보드 → README 시작 가이드 → Report/Transcript Export 세션._

_Exported on 2026-05-29._

---

**User**

- `@Report/` 폴더 참고하여 테스트 플랜 작성용 **샘플 예제 1건** 선택.
- 선택 기준:
  1. PRD FR-01 AC 중 가장 선행 — 입력 유효성 검사
  2. `grid is None` → `INVALID_SIZE` 비즈니스 로직 직접 검증
  3. Boundary + Domain 진입점 호출 격리 동시 검증 가능
- 출력: AC ID, PRD 번호, 입력/기대 출력, 선택 이유 2줄.
- **코드 작성 금지**, 선택 결과 문서만.

**Assistant**

- `Report/02` **S-011**, PRD **AC-FR01-01**, **FR-01** §12.1·§13.2·§16 ES-01 선정.
- 입력: `grid = None`
- 기대(플랜 샘플): `INVALID_SIZE` / `Grid must be 4x4.`
- PRD 공식: `ERR_INVALID_SHAPE` (명칭 매핑 필요함을 명시).
- 선택 이유: I-1 선행 형태 검증 + BR-05 Domain 미호출 동시 검증.

---

**User**

- 지금까지 모든 내용을 이용하여 **to list** 만들어 달라.

**Assistant**

- Phase 0~7 통합 To-Do (PRD v0.2, Dual-Track, TASK 매핑, P0 우선순위).
- 이전 대화·Report/07·선택 샘플·FR-01~05 반영.

---

**User**

- **다시** 작성 요청 — Senior Architect + Dual-Track TDD 코치 역할.
- PRD 기반 **개발 To-Do List** = Scenario→AC→RED→Test Skeleton→Run→RED 확인→GREEN 후보→REFACTOR 후보 추적 보드.
- 구현·테스트·파일 생성 금지, Markdown만.
- 표 형식: Epic, US, Tracking Board (TASK-001~), RED Start Checklist, Traceability Summary.
- 필수 Scenario 15항목 포함.

**Assistant**

- `# MagicSquare 4x4 개발 To-Do List` 출력.
- Epic-001, US-001~006, TASK-001~021 Tracking Board 표.
- Track: Boundary RED / Logic RED / Integration RED.
- RED = 실패 상태 확인, GREEN = 최소 구현 **후보**, REFACTOR = 구조 개선 **후보**만.
- Traceability Summary 16 Concept 행.
- OPEN: TD-02, TD-07 행렬 미확정.

---

**User**

- **Technical Writer** 역할로 MagicSquare 4×4 **README.md 초안** 작성.
- PRD 기반 프로젝트 **시작 선언** + TDD 8단계 흐름 개발 가이드.
- §1~§10 구조 (Project Start, PRD Summary, TDD Flow, Methodology, ECB, Tracking Board, Checklist, Quality Gates, References, Status).
- §6 Tracking Board에 필수 Scenario 15항목.
- 구현·테스트·파일 생성 금지, README 본문 Markdown만.

**Assistant**

- `# MagicSquare 4x4 TDD Practice` README 초안 10섹션 출력.
- RED = 테스트 실패 확인 단계 명시.
- SC-BND-001~007, SC-DOM-001~008 Tracking 표.
- 문서 경로: `docs/PRD_MagicSquare.md`, Report/01~07, `.cursor/rules/*.mdc`.
- 현재 상태: PRD 준비 완료, 마방진 구현·RED 테스트 미착수.

---

**User (Current Request)**

- **Report** 폴더에 보고서 생성.
- **Prompt** 폴더에 Transcript Export.

**Assistant**

- `Report/08MagicSquare-TDD-Start-ToDo-README-Report.md` 생성.
- `Prompt/08cursor_magicsquare_tdd_start_todo_readme_transcript.md` 생성.
- `Report/README.md` 인덱스 갱신.

---

## Exported Artifacts

| 유형 | 경로 |
|------|------|
| Report | `Report/08MagicSquare-TDD-Start-ToDo-README-Report.md` |
| Transcript | `Prompt/08cursor_magicsquare_tdd_start_todo_readme_transcript.md` |

## Session Decisions (요약)

| 항목 | 결정 |
|------|------|
| 테스트 플랜 샘플 | AC-FR01-01, `grid=None`, Report/02 S-011 |
| 추적 보드 | TASK-001~021, RED-BND/DOM/INT ID |
| README | 10섹션 초안 (루트 미저장) |
| 구현 상태 | 마방진 도메인·RED 테스트 **미착수** |

## Next Step (권장)

1. OPEN-01 에러 코드 통일  
2. Test Skeleton → `pytest` → Confirm Failure = RED (`RED-BND-001`)  
3. 루트 README 병합 (선택)
