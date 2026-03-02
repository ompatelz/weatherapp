# Concerns: India Energy Atlas

## Technical Debt

| Concern | Severity | Detail |
|---------|----------|--------|
| Mock data only | Medium | All 12 states use hardcoded data in `mock_data.py` — no real data ingestion |
| No database | Medium | Data lives in Python dicts; no persistence layer |
| No tests | Medium | Zero automated tests for frontend or backend |
| No error boundaries | Low | Frontend has no React error boundaries |
| GeoJSON from external URL | Low | State boundaries fetched from GitHub on each map load |

## Architectural Concerns

- **Scaling** — Mock data pattern won't scale; needs database + data pipeline
- **State coverage** — Only 12 of 28+ states have data; remaining states click but show nothing
- **No loading/error UI for API failures** — If backend is down, panel shows nothing silently

## Security

- **CORS** — Currently allows `http://localhost:3000` only (good for dev)
- **No auth** — API is fully public (acceptable for Phase 1)
- **No input validation** — FastAPI handles basic type checking via path params

## Performance

- **GeoJSON** — ~1MB file loaded on every page visit (should be cached or bundled)
- **No code splitting** — Beyond the dynamic import of `IndiaMap`, no further splitting
