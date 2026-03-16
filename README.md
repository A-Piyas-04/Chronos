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

### Environment Setup

- Copy env templates (safe defaults):
  - Root: copy `.env.example` → `.env` (Postgres credentials)
  - Web: copy `apps/web/.env.example` → `apps/web/.env`
  - API: copy `apps/api/.env.example` → `apps/api/.env`
  - Worker: copy `apps/worker/.env.example` → `apps/worker/.env`
- Sentry is optional:
  - Backend: set `SENTRY_DSN` to enable Sentry
  - Frontend client: set `NEXT_PUBLIC_SENTRY_DSN` to enable Sentry in the browser

### Run Everything (One Command)

```bash
docker compose up --build
```

- Web: http://localhost:3000
- API: http://localhost:8000/health

### Common Commands

```bash
docker compose ps
docker compose logs -f api
docker compose down
```

### Run Services Individually (Optional)

- Web:
  - `cd apps/web`
  - `npm run dev`
- API:
  - `cd apps/api`
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Worker:
  - `cd apps/worker`
  - `celery -A worker.celery_app worker --loglevel=info`

## Engineering Standards

### IDs

All major entities must use UUID v4 (not incremental IDs).

### Timezones

- Store all timestamps in UTC at rest.
- Convert to the user’s timezone at the API boundary (request/response layer).
