# Structure: India Energy Atlas

## Directory Tree

```
web/
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, CORS, router mount
│   ├── requirements.txt           # fastapi, uvicorn
│   ├── routers/
│   │   ├── __init__.py
│   │   └── energy.py              # GET /api/states, GET /api/states/{id}
│   └── services/
│       ├── __init__.py
│       └── mock_data.py           # Hardcoded data for 12 Indian states
│
└── frontend/
    ├── .env.local                 # NEXT_PUBLIC_API_URL
    ├── app/
    │   ├── globals.css            # Tailwind import, Mapbox overrides
    │   ├── layout.tsx             # Root layout (Inter font, dark theme)
    │   └── page.tsx               # Main page — map + panel composition
    ├── components/
    │   ├── IndiaMap.tsx            # MapLibre GL JS map component
    │   ├── StatePanel.tsx         # Slide-in detail panel
    │   ├── EnergyMixChart.tsx     # Recharts PieChart (donut)
    │   └── TrendChart.tsx         # Recharts LineChart
    ├── lib/
    │   ├── api.ts                 # fetchStates(), fetchStateDetail()
    │   ├── constants.ts           # STATE_NAME_TO_ID, GEOJSON URL, colors
    │   └── types.ts               # StateSummary, StateDetail, etc.
    ├── next.config.ts
    ├── tailwind.config.ts
    ├── tsconfig.json
    └── package.json
```

## File Counts

| Directory | Files | Purpose |
|-----------|-------|---------|
| `web/backend/` | 6 | API server + mock data |
| `web/frontend/app/` | 3 | Pages + layout |
| `web/frontend/components/` | 4 | UI components |
| `web/frontend/lib/` | 3 | Utilities + types |
| **Total** | **~16 source files** | |

## Key Entry Points

- **Frontend entry:** `web/frontend/app/page.tsx`
- **Backend entry:** `web/backend/main.py`
- **Data source:** `web/backend/services/mock_data.py`
