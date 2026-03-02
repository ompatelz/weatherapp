# Roadmap: India Energy Atlas

## Overview

Build an interactive energy data visualization platform for India, starting with a mock-data MVP and evolving toward real government data, enhanced features, and production deployment.

## Milestones

- ✅ **v1.0 MVP** — Phases 1 (shipped 2026-02-14)
- 📋 **v1.1 Real Data** — Phases 2 (planned)
- 📋 **v2.0 Enhanced Features** — Phases 3–4 (planned)

## Phases

<details>
<summary>✅ v1.0 MVP (Phase 1) — SHIPPED 2026-02-14</summary>

### Phase 1: Foundation & MVP
**Goal**: Ship a working interactive map with state-level energy data panels
**Depends on**: Nothing (first phase)
**Requirements**: MAP-01–04, DATA-01–04, UI-01–04, API-01–03
**Success Criteria** (what must be TRUE):
  1. Map loads with India state boundaries on a dark theme
  2. Clicking a state shows a slide-in panel with capacity, generation, energy mix chart, and trend chart
  3. API returns correct data for all 12 mock states
  4. UI is responsive and professional
**Plans**: 3 plans

Plans:
- [x] 01-01: Backend scaffolding — FastAPI + mock data + REST endpoints
- [x] 01-02: Frontend scaffolding — Next.js 14 + MapLibre map + chart components
- [x] 01-03: Integration & polish — Wire up page, panel, charts, verify end-to-end

</details>

### 📋 v1.1 Real Data

#### Phase 2: Real Data Pipeline
**Goal**: Replace mock data with actual Indian energy statistics
**Depends on**: Phase 1
**Requirements**: RDATA-01, RDATA-02, INFRA-01
**Success Criteria** (what must be TRUE):
  1. Data sourced from CEA/POSOCO or equivalent government API
  2. All 28 states and 8 union territories have energy data
  3. PostgreSQL stores state energy data persistently
  4. Data can be updated without redeploying
**Plans**: TBD

Plans:
- [ ] 02-01: Database setup — PostgreSQL schema + data models
- [ ] 02-02: Data ingestion — Scraper/ETL for government energy data
- [ ] 02-03: API migration — Switch endpoints from mock data to database

### 📋 v2.0 Enhanced Features

#### Phase 3: Advanced Visualization
**Goal**: Add comparison, search, ranking, and choropleth features
**Depends on**: Phase 2
**Requirements**: FEAT-01, FEAT-02, FEAT-03, FEAT-04
**Success Criteria** (what must be TRUE):
  1. Users can compare two states side-by-side
  2. Search bar filters states by name
  3. State ranking table sortable by capacity/generation
  4. Map colors states by selected metric (choropleth)
**Plans**: TBD

Plans:
- [ ] 03-01: Search & filter — State search bar + autocomplete
- [ ] 03-02: Comparison mode — Side-by-side state comparison panel
- [ ] 03-03: Rankings & choropleth — Data table + color-coded map

#### Phase 4: Testing & Deployment
**Goal**: Add automated tests and production deployment
**Depends on**: Phase 3
**Requirements**: INFRA-02, INFRA-03
**Success Criteria** (what must be TRUE):
  1. Backend tests pass (pytest)
  2. Frontend tests pass (React Testing Library)
  3. Docker Compose runs both services
**Plans**: TBD

Plans:
- [ ] 04-01: Automated tests — pytest + RTL test suites
- [ ] 04-02: Docker — Dockerfiles + docker-compose.yml

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & MVP | 3/3 | Complete | 2026-02-14 |
| 2. Real Data Pipeline | 0/3 | Not started | - |
| 3. Advanced Visualization | 0/3 | Not started | - |
| 4. Testing & Deployment | 0/2 | Not started | - |
