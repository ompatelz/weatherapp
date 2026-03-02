# Testing: India Energy Atlas

## Current State

**No automated tests exist yet.**

- No test framework configured (frontend or backend)
- No CI/CD pipeline

## Recommended Setup

### Frontend
- **Framework:** Jest + React Testing Library (or Vitest)
- **Priority tests:**
  - `lib/api.ts` — Mock `fetch`, verify URL construction and error handling
  - `components/StatePanel.tsx` — Render with mock `StateDetail`, verify cards + charts
  - `lib/constants.ts` — Verify `STATE_NAME_TO_ID` mapping completeness

### Backend
- **Framework:** pytest + httpx (FastAPI's TestClient)
- **Priority tests:**
  - `GET /api/states` returns 200 with 12 items
  - `GET /api/states/maharashtra` returns correct structure
  - `GET /api/states/invalid` returns 404

## Manual Verification (Currently Used)

- HTTP requests via `Invoke-WebRequest` to verify API responses
- Browser visual check for frontend rendering
- Next.js dev server compilation check (no TypeScript errors)
