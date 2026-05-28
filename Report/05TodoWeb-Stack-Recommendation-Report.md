# TODO Web 기술 스택 추천 보고서

## 1) 목적

간단한 TODO 리스트 기능을 웹페이지 형태로 구현할 때,
개발 속도, 유지보수성, 확장성을 균형 있게 만족하는 기술 스택을 제안한다.

## 2) 요구사항 해석

- 대상: 단순 TODO CRUD 중심의 웹 UI
- 우선순위: 빠른 구현, 낮은 복잡도, 쉬운 유지보수
- 선택 기준: 초기 생산성, 학습 비용, 향후 확장 가능성

## 3) 검토 결과

- `Next.js`는 SSR/라우팅/풀스택 기능이 강점이지만, 단순 TODO에는 과한 선택일 수 있음
- `Vanilla JS`는 가장 가볍지만 규모 확장 시 구조화와 상태 관리가 어려워질 수 있음
- `React + TypeScript + Vite`는 구현 속도와 확장성의 균형이 가장 좋음

## 4) 권장 기본 스택

- Frontend: `React + TypeScript + Vite`
- Styling: `Tailwind CSS` (또는 CSS Modules)
- State: `useState` 중심 (필요 시 `Zustand` 확장)
- Storage: `localStorage` (브라우저 단독 앱 기준)
- Test: `Vitest + React Testing Library`
- Deploy: `Vercel` 또는 `Netlify`

## 5) 대안 선택 가이드

- 초학습/초경량이 최우선: `HTML + CSS + Vanilla JS + localStorage`
- 로그인/동기화/API 연동까지 계획: 권장 기본 스택 + 백엔드(`Node.js`, `Supabase`, `Firebase` 등)

## 6) 결론

현재 요구 범위(간단한 TODO 웹페이지)에서는
`React + TypeScript + Vite + localStorage` 조합이 가장 합리적이며,
기능 확장 시에도 구조를 크게 바꾸지 않고 성장시킬 수 있다.
