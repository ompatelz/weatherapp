# Requirements: India Energy Atlas

**Defined:** 2026-02-13
**Core Value:** Users can instantly explore energy profiles of Indian states through an interactive map

## v1 Requirements

### Map & Navigation

- [x] **MAP-01**: User sees an interactive dark-themed map of India on page load
- [x] **MAP-02**: States are highlighted with boundaries on the map
- [x] **MAP-03**: Hovering a state visually highlights it (cyan fill)
- [x] **MAP-04**: Clicking a state selects it and triggers data load

### Data Display

- [x] **DATA-01**: Selected state shows installed capacity (MW) in a summary card
- [x] **DATA-02**: Selected state shows generation (GWh) in a summary card
- [x] **DATA-03**: Energy mix displayed as a donut pie chart (Thermal, Solar, Wind, Hydro, Nuclear)
- [x] **DATA-04**: Generation trend displayed as a line chart (2020–2024)

### Panel & UI

- [x] **UI-01**: State detail panel slides in from the right
- [x] **UI-02**: Panel includes close button to dismiss
- [x] **UI-03**: Loading spinner shown while fetching state data
- [x] **UI-04**: Dark premium design with responsive layout

### Backend

- [x] **API-01**: GET /api/states returns list of all states with summary
- [x] **API-02**: GET /api/states/{id} returns full detail including energy mix and trend
- [x] **API-03**: Invalid state ID returns 404

## v2 Requirements

### Real Data

- **RDATA-01**: Ingest real energy data from CEA/POSOCO sources
- **RDATA-02**: Cover all 28 states and 8 union territories
- **RDATA-03**: Data updated monthly or quarterly

### Enhanced Features

- **FEAT-01**: State comparison mode (select 2 states side-by-side)
- **FEAT-02**: Search bar to find states by name
- **FEAT-03**: State ranking table (sortable by capacity/generation)
- **FEAT-04**: Choropleth coloring based on a selected metric

### Infrastructure

- **INFRA-01**: PostgreSQL database for persistent data storage
- **INFRA-02**: Automated tests (pytest + React Testing Library)
- **INFRA-03**: Docker deployment configuration

## Out of Scope

| Feature | Reason |
|---------|--------|
| User accounts / auth | Public data, no personalization needed |
| Real-time streaming | Energy data is periodic, not real-time |
| Mobile native app | Web responsive is sufficient |
| District-level data | State level is the primary unit |
| Historical data before 2020 | Limited value, keep scope narrow |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| MAP-01 | Phase 1 | Complete |
| MAP-02 | Phase 1 | Complete |
| MAP-03 | Phase 1 | Complete |
| MAP-04 | Phase 1 | Complete |
| DATA-01 | Phase 1 | Complete |
| DATA-02 | Phase 1 | Complete |
| DATA-03 | Phase 1 | Complete |
| DATA-04 | Phase 1 | Complete |
| UI-01 | Phase 1 | Complete |
| UI-02 | Phase 1 | Complete |
| UI-03 | Phase 1 | Complete |
| UI-04 | Phase 1 | Complete |
| API-01 | Phase 1 | Complete |
| API-02 | Phase 1 | Complete |
| API-03 | Phase 1 | Complete |
| RDATA-01 | Phase 2 | Pending |
| RDATA-02 | Phase 2 | Pending |
| FEAT-01 | Phase 3 | Pending |
| FEAT-02 | Phase 3 | Pending |
| FEAT-03 | Phase 3 | Pending |
| FEAT-04 | Phase 3 | Pending |
| INFRA-01 | Phase 2 | Pending |
| INFRA-02 | Phase 4 | Pending |
| INFRA-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-13*
*Last updated: 2026-02-14 after Phase 1 completion*
