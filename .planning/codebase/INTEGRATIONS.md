# Integrations: India Energy Atlas

## External Services

| Service | Type | Auth Required | Purpose |
|---------|------|---------------|---------|
| CARTO Basemaps | Tile server | No | Dark vector map tiles (`dark-matter-gl-style`) |
| GitHub Raw Content | Static file | No | India GeoJSON state boundaries |

## Internal Integration Points

| From | To | Protocol | Port |
|------|----|----------|------|
| Next.js frontend | FastAPI backend | HTTP REST | 3000 → 8000 |
| MapLibre GL JS | CARTO CDN | HTTPS | External |
| MapLibre GL JS | GitHub Raw | HTTPS | External |

## Future Integration Candidates

- **Real energy data API** — Replace mock_data.py with actual government data source (e.g., CEA, POSOCO)
- **Database** — PostgreSQL/PostGIS for persistent state-level energy data
- **Authentication** — If admin features are added
