# Conventions: India Energy Atlas

## Code Style

| Aspect | Convention |
|--------|-----------|
| Frontend language | TypeScript (strict) |
| Component style | Functional components with hooks |
| Directive | `"use client"` on all interactive components |
| Exports | Default exports for components |
| Naming — files | PascalCase for components, camelCase for utilities |
| Naming — variables | camelCase |
| Naming — types | PascalCase interfaces |

## Patterns

- **Dynamic imports** for browser-only libraries (`next/dynamic` with `ssr: false`)
- **`useCallback`** for event handlers passed to child components
- **`useRef`** for map instance and DOM containers
- **Typed fetch functions** in `lib/api.ts` wrapping `fetch()`
- **Constants mapping** for GeoJSON-to-backend ID translation

## Backend Patterns

- **Router-based structure** — `routers/energy.py` mounted at prefix
- **Service layer** — `services/mock_data.py` separates data from routes
- **CORS middleware** — Configured in `main.py`
- **HTTP 404** — Raised when state ID not found

## Styling

- TailwindCSS utility classes inline
- Dark theme (`bg-slate-950`, `text-slate-100`)
- Cyan accent palette (`cyan-400`, `cyan-500`)
- Custom scrollbar CSS in `globals.css`
