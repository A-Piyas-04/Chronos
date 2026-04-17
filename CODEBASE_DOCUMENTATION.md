# Chronos Codebase Documentation

## 1) Project Overview

Chronos is a monorepo scaffold for an AI-powered time and life management platform. It currently contains:

- A web frontend (`Next.js` + `React` + `TypeScript`)
- An API service (`FastAPI` + `SQLAlchemy`)
- A background worker (`Celery` + `Redis`)
- Local orchestration (`Docker Compose` with `PostgreSQL` and `Redis`)

Current status: the repository is a strong production-ready foundation with health checks, observability hooks, tooling configs, and environment templates, but domain/business features are still minimal.

## 2) Repository Structure

```text
Chronos/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── CODEBASE_DOCUMENTATION.md
└── apps/
    ├── api/
    │   ├── .env.example
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    │       ├── config.py
    │       ├── database.py
    │       ├── health.py
    │       ├── main.py
    │       └── utils/
    │           ├── time.py
    │           └── uuid.py
    ├── worker/
    │   ├── .env.example
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── worker/
    │       ├── celery_app.py
    │       └── tasks.py
    └── web/
        ├── .env.example
        ├── .gitignore
        ├── .prettierignore
        ├── .prettierrc.json
        ├── Dockerfile
        ├── README.md
        ├── eslint.config.mjs
        ├── next.config.ts
        ├── package-lock.json
        ├── package.json
        ├── sentry.client.config.ts
        ├── sentry.edge.config.ts
        ├── sentry.server.config.ts
        ├── tsconfig.json
        ├── app/
        │   ├── globals.css
        │   ├── layout.tsx
        │   ├── page.module.css
        │   └── page.tsx
        └── public/
            ├── file.svg
            ├── vercel.svg
            └── window.svg
```

## 3) What Is Implemented

## 3.1 Root / Infrastructure

- `docker-compose.yml` defines and wires five services:
  - `postgres` (`postgres:16-alpine`)
  - `redis` (`redis:7-alpine`)
  - `api` (builds from `apps/api`)
  - `worker` (builds from `apps/worker`)
  - `web` (builds from `apps/web`)
- Health checks are configured for `postgres` and `redis`.
- `api` starts after healthy `postgres` and `redis`.
- `worker` starts after healthy `redis`.
- `web` depends on `api`.
- Persistent volume: `postgres_data`.
- Isolated web dependency volume: `web_node_modules`.

## 3.2 API Service (`apps/api`)

### Entrypoint and app setup

- `app/main.py`
  - Loads settings via `get_settings()`.
  - Initializes Sentry if `SENTRY_DSN` is provided.
  - Creates `FastAPI(title="Chronos API")`.
  - Includes health router.

### Configuration

- `app/config.py`
  - Loads environment via `python-dotenv`.
  - Defines `Settings` model (`pydantic`) for:
    - `ENVIRONMENT`
    - `DATABASE_URL`
    - `SENTRY_DSN`
  - Caches settings via `@lru_cache`.

### Database

- `app/database.py`
  - Creates SQLAlchemy engine from `DATABASE_URL`.
  - Uses `pool_pre_ping=True`.
  - Implements readiness probe query (`SELECT 1`).

### Routes

- `app/health.py`
  - `GET /health` returns `{ "status": "ok" }`
  - `GET /ready` checks DB connectivity and returns:
    - `200` + `{ "status": "ok" }` if ready
    - `503` + `detail="not ready"` if not ready

### Utilities

- `app/utils/time.py`
  - UTC time helper(s) and timezone conversion helper(s) for API boundary handling.
- `app/utils/uuid.py`
  - UUID v4 generator helper(s).

## 3.3 Worker Service (`apps/worker`)

### Celery app

- `worker/celery_app.py`
  - Loads `.env`.
  - Uses `CELERY_BROKER_URL` (default `redis://redis:6379/0`).
  - Creates Celery app: `chronos_worker`.
  - Autodiscovers tasks in `worker.tasks`.

### Tasks

- `worker/tasks.py`
  - Defines sample task `worker.example_task`.
  - Logs execution.
  - Returns `"ok"`.

## 3.4 Web Service (`apps/web`)

### App shell and page

- `app/layout.tsx`
  - Root layout with metadata and font setup.
- `app/page.tsx`
  - Placeholder UI page displaying "Chronos Web App".
- `app/globals.css`, `app/page.module.css`
  - Global + module styling.

### Runtime config

- `next.config.ts`
  - Enables `reactCompiler: true`.

### Observability

- `sentry.client.config.ts`
  - Browser-side Sentry using `NEXT_PUBLIC_SENTRY_DSN`.
- `sentry.edge.config.ts` and `sentry.server.config.ts`
  - Edge/server Sentry setup using `SENTRY_DSN`.

## 4) Dependency Inventory

## 4.1 Web Dependencies (`apps/web/package.json`)

### Runtime dependencies

- `@sentry/nextjs`: `^10.43.0`
- `next`: `16.1.6`
- `react`: `19.2.3`
- `react-dom`: `19.2.3`

### Development dependencies

- `@types/node`: `^20`
- `@types/react`: `^19`
- `@types/react-dom`: `^19`
- `babel-plugin-react-compiler`: `1.0.0`
- `eslint`: `^9`
- `eslint-config-next`: `16.1.6`
- `prettier`: `^3.8.1`
- `typescript`: `^5`

### Lockfile

- `apps/web/package-lock.json` is present (npm lockfile v3), so Node dependencies are reproducible.

## 4.2 API Dependencies (`apps/api/requirements.txt`)

- `fastapi`
- `uvicorn[standard]`
- `pydantic`
- `sqlalchemy`
- `psycopg2-binary`
- `python-dotenv`
- `sentry-sdk`
- `ruff`
- `black`
- `mypy`

Note: versions are currently not pinned in `requirements.txt`.

## 4.3 Worker Dependencies (`apps/worker/requirements.txt`)

- `celery`
- `redis`
- `python-dotenv`

Note: versions are currently not pinned in `requirements.txt`.

## 4.4 Tooling Configuration

- `pyproject.toml` configures:
  - `black` (line length 88, `py311`)
  - `ruff` (selected rules: `E`, `F`, `I`, `B`, `UP`)
  - `mypy` (Python 3.11 with strictness options)
- `apps/web/eslint.config.mjs` configures linting for Next.js.
- `apps/web/.prettierrc.json` configures formatting.

## 5) Environment Variables and Runtime Inputs

## 5.1 Root

From `.env.example`:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

## 5.2 API

From `apps/api/.env.example`:

- `ENVIRONMENT`
- `DATABASE_URL`
- `SENTRY_DSN`

## 5.3 Worker

From `apps/worker/.env.example`:

- `ENVIRONMENT`
- `CELERY_BROKER_URL`
- `SENTRY_DSN`

## 5.4 Web

From `apps/web/.env.example`:

- `NEXT_PUBLIC_API_URL`
- `SENTRY_DSN`
- `NEXT_PUBLIC_SENTRY_DSN`

## 6) Build and Run Details

## 6.1 Docker images used

- API: `python:3.11-slim`
- Worker: `python:3.11-slim`
- Web: `node:20-alpine`
- Postgres: `postgres:16-alpine`
- Redis: `redis:7-alpine`

## 6.2 Service command behavior

- API container starts `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Worker container starts `celery -A worker.celery_app worker --loglevel=info`
- Web container starts `npm run dev -- -H 0.0.0.0 -p 3000`

## 6.3 Web scripts

From `apps/web/package.json`:

- `npm run dev`
- `npm run build`
- `npm run start`
- `npm run lint`
- `npm run format`
- `npm run format:check`

## 7) Current Gaps / Incomplete Areas

- API currently exposes foundational health/readiness endpoints only.
- Worker currently includes one example task only.
- Web currently shows a placeholder page and does not yet consume API data.
- No test suites are present yet (backend or frontend).
- No CI workflow files are present in the repository.
- README references `packages/*` and `infra/docker`, but those paths are not currently present.

## 8) Architecture Summary

Current interaction model in local development:

1. `docker compose up --build` boots database/cache first.
2. API starts and provides health/readiness checks.
3. Worker connects to Redis and waits for tasks.
4. Web app starts in dev mode and is available at port 3000.

This provides a production-oriented baseline architecture with observability hooks and developer tooling, ready for domain feature implementation.
