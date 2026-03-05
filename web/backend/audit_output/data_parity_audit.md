# India Energy Atlas — Data Parity Audit

**Date:** 2026-03-03 23:06:47
**Base URL:** http://127.0.0.1:8000

## Local Data Summary

| Metric | Value |
|---|---|
| States | 37 |
| State-year data points | 296 |
| Power plants | 3801 |
| Correlation errors | 2 |

### Correlation Year Errors

- Year **2025**: HTTP 400
- Year **2026**: HTTP 400

## Live Endpoint Checks

| Endpoint | Status |
|---|---|
| /api/generation/live | timestamp=`Live`, national=330248 MW |
| /api/market/pricing/live | timestamp=`2026-02-28T12:00:00Z` |

## Wikipedia Capacity Parity (2025 snapshot)

| State | Local (GW) | Wiki Approx (GW) | Gap (%) |
|---|---|---|---|
| karnataka | 26.25 | 18 | 45.83% ⚠️ |
| tamil_nadu | 27.3 | 20 | 36.5% ⚠️ |
| andhra_pradesh | 19.9 | 16 | 24.37% ⚠️ |
| uttar_pradesh | 18.59 | 15 | 23.93% ⚠️ |
| madhya_pradesh | 18.22 | 15 | 21.47% ⚠️ |
| rajasthan | 24.36 | 30 | 18.8% ⚠️ |
| maharashtra | 27.72 | 25 | 10.88% ⚠️ |
| telangana | 12.97 | 12 | 8.08% |
| gujarat | 26.09 | 25 | 4.36% |

**Mean gap:** 21.58%
**States above 10% gap:** 7

## Observations

- Analytics correlation returned errors for years: [2025, 2026]. Backend may not support those years.
- /api/generation/live uses a fixed 'Live' timestamp — this is simulation-style output.
- Capacity vs Wikipedia approx: 9 states checked, mean abs gap 21.58%, 7 states above 10% gap.
- Local power plant count: 3801
- Report generated: 2026-03-03 23:06. Data freshness depends on last scraper run.