# India Energy Atlas — Stress Test Report

**Date:** 2026-03-03 23:06:46
**Base URL:** http://127.0.0.1:8000
**Endpoints tested:** 17
**Concurrency levels:** [50, 100, 250, 500, 1000]

## Summary Table

| Concurrency | RPS | Mean (s) | Median (s) | P95 (s) | P99 (s) | Max (s) | Errors | HTTP 4xx/5xx |
|---|---|---|---|---|---|---|---|---|
| 50 | 129.28 | 0.3868 | 0.3912 | 0.4007 | 0.4047 | 0.4047 | 0 | 0 |
| 100 | 192.46 | 0.5196 | 0.5828 | 0.6956 | 0.7028 | 0.7028 | 0 | 0 |
| 250 | 221.62 | 1.1281 | 1.1724 | 1.736 | 1.7583 | 1.7631 | 0 | 0 |
| 500 | 236.65 | 2.1129 | 2.14 | 3.6093 | 3.7445 | 3.7751 | 0 | 0 |
| 1000 | 235.51 | 4.2461 | 4.2628 | 7.3937 | 7.7067 | 7.8309 | 0 | 0 |

> [!WARNING]
> Breaking behavior observed at **1000 concurrent users** (P95=7.3937s, errors=0).

## Error Breakdown


## Observations

- Peak throughput: **236.65 RPS** at concurrency 500
- `/api/generation/live` and `/api/market/pricing/live` produce randomized simulation data.
- Tested 17 endpoints covering states, power plants, analytics, generation, and market.