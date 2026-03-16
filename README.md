# Chronos

Production-grade development foundation for Chronos, an AI-powered time and life management platform.

## Monorepo Layout

- `apps/web` — Next.js (TypeScript) frontend
- `apps/api` — FastAPI backend
- `apps/worker` — Celery worker
- `packages/*` — shared packages (types/config)
- `infra/docker` — Docker-related infra

## Branch Strategy

- `main` — production-ready
- `dev` — integration branch
- `feature/*` — feature work branched from `dev`, merged back into `dev`

## Local Development

### Prerequisites

- Docker + Docker Compose

### Run Everything

```bash
docker-compose up --build
```

- Web: http://localhost:3000
- API: http://localhost:8000/health

## Engineering Standards

### IDs

All major entities must use UUID v4 (not incremental IDs).

### Timezones

- Store all timestamps in UTC at rest.
- Convert to the user’s timezone at the API boundary (request/response layer).
