# Stack: India Energy Atlas

## Runtime & Language

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend runtime | Node.js | ≥18 |
| Frontend framework | Next.js (App Router) | 16.1.6 |
| Language | TypeScript | 5.x |
| Styling | TailwindCSS | v4 (via `@import "tailwindcss"`) |
| Map library | MapLibre GL JS | latest |
| Charts | Recharts | latest |
| Backend runtime | Python | 3.x |
| Backend framework | FastAPI | 0.109.2 |
| ASGI server | Uvicorn | 0.27.1 |

## Package Manager

- **Frontend:** npm (package-lock.json present)
- **Backend:** pip (requirements.txt)

## Build & Dev

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start Next.js dev server on :3000 |
| `python -m uvicorn main:app --reload --port 8000` | Start FastAPI dev server on :8000 |

## Key Dependencies

### Frontend (`web/frontend/package.json`)
- `next` — App Router framework
- `react`, `react-dom` — UI runtime
- `maplibre-gl` — Free vector map (Mapbox drop-in replacement)
- `recharts` — Pie chart, line chart components
- `typescript` — Type safety

### Backend (`web/backend/requirements.txt`)
- `fastapi` — REST API framework
- `uvicorn[standard]` — ASGI server with hot reload

## Environment Variables

| Variable | File | Purpose |
|----------|------|---------|
| `NEXT_PUBLIC_API_URL` | `web/frontend/.env.local` | Backend API base URL |
