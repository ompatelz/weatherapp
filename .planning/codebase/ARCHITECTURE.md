# Architecture: India Energy Atlas

## System Overview

```
┌──────────────────────────────────────────┐
│              User's Browser              │
│  ┌────────────────────────────────────┐  │
│  │  Next.js App (localhost:3000)      │  │
│  │  ┌──────────┐  ┌───────────────┐  │  │
│  │  │ IndiaMap  │  │  StatePanel   │  │  │
│  │  │(MapLibre) │  │  EnergyMix ▪  │  │  │
│  │  │          ──→│  TrendChart▪  │  │  │
│  │  └──────────┘  └───────────────┘  │  │
│  └────────────────────────────────────┘  │
│              │ fetch()                    │
│              ▼                            │
│  ┌────────────────────────────────────┐  │
│  │  FastAPI Backend (localhost:8000)  │  │
│  │  GET /api/states                   │  │
│  │  GET /api/states/{id}              │  │
│  │  └─→ mock_data.py (in-memory)     │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## Data Flow

1. **Page load** → `IndiaMap` renders MapLibre GL JS with CARTO dark tiles
2. **GeoJSON load** → State boundaries fetched from GitHub (raw GeoJSON)
3. **User clicks state** → `NAME_1` property mapped to backend `state_id` via `STATE_NAME_TO_ID`
4. **API call** → `fetchStateDetail(stateId)` hits `GET /api/states/{id}`
5. **Panel renders** → `StatePanel` slides in with capacity cards, `EnergyMixChart`, `TrendChart`

## Rendering Strategy

- **Server-side layout** — `layout.tsx` is a Server Component (metadata, fonts)
- **Client-side page** — `page.tsx` uses `"use client"` for state + fetch
- **Dynamic import** — `IndiaMap` loaded via `next/dynamic` with `{ ssr: false }` (MapLibre needs DOM)

## API Design

| Method | Endpoint | Response |
|--------|---------|----------|
| GET | `/api/states` | `StateSummary[]` — id, name, capacity, generation |
| GET | `/api/states/{id}` | `StateDetail` — full detail + energy_mix + trend |
| 404 | `/api/states/{invalid}` | `{"detail": "State not found"}` |

CORS is configured to allow `http://localhost:3000`.
