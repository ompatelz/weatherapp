# India Energy Atlas

## What This Is

India Energy Atlas is an interactive web application that visualizes state-level energy data across India. Users click states on a dark-themed map to view installed capacity, generation, energy mix (pie chart), and generation trends (line chart) in a slide-in panel. Built with Next.js 14 + FastAPI, currently using mock data for 12 states.

## Core Value

Users can instantly explore and compare energy profiles of Indian states through an interactive map — no login, no setup, one click.

## Requirements

### Validated

- ✓ Interactive map of India with state boundaries — Phase 1
- ✓ Click state → slide-in panel with energy data — Phase 1
- ✓ Energy mix pie chart (Recharts) — Phase 1
- ✓ Generation trend line chart (Recharts) — Phase 1
- ✓ FastAPI backend with REST endpoints — Phase 1
- ✓ Dark premium UI with responsive layout — Phase 1
- ✓ Free map tiles (MapLibre, no API key) — Phase 1

### Active

- [ ] Real energy data from government sources (CEA/POSOCO)
- [ ] All 28+ states and 8 UTs covered
- [ ] State comparison mode (side-by-side)
- [ ] Search/filter by state name
- [ ] Database persistence (PostgreSQL)

### Out of Scope

- Mobile native app — Web-first, responsive design is sufficient
- User authentication — Public data, no login needed
- Real-time data streaming — Static/periodic data is fine for energy stats
- Offline mode — Requires internet for map tiles

## Context

- India has 28 states and 8 union territories with varied energy profiles
- Government data available from CEA (Central Electricity Authority) and NITI Aayog
- Current mock data covers: Maharashtra, Gujarat, Tamil Nadu, Rajasthan, Karnataka, Uttar Pradesh, Andhra Pradesh, Madhya Pradesh, Telangana, Punjab, West Bengal, Kerala
- GeoJSON source uses `NAME_1` property for state names

## Constraints

- **Tech Stack**: Next.js 14 + FastAPI — already committed
- **No API Keys**: MapLibre GL JS with free CARTO tiles — zero cost
- **Data Accuracy**: Mock data only for now — real data integration is Phase 2
- **Browser Support**: Modern browsers with WebGL support (for MapLibre)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| MapLibre over Mapbox | Free, no token, identical API | ✓ Good |
| CARTO dark-matter tiles | Free, dark theme, professional look | ✓ Good |
| Recharts for charts | Lightweight, React-native, good defaults | ✓ Good |
| FastAPI for backend | Fast dev, auto-docs, async-ready | ✓ Good |
| Mock data first | Ship fast, validate UX before data pipeline | ✓ Good |
| GeoJSON from GitHub | Free, reliable, avoids bundling ~1MB | ⚠️ Revisit (bundle for prod) |

---
*Last updated: 2026-02-14 after Phase 1 completion*
