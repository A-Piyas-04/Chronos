# Chronos — Phase 1 Implementation Plan (Deterministic MVP)

This document is the engineering plan for **Phase 1** only: auth + onboarding, read-only Google Calendar sync, task inbox, a **deterministic** scheduler (no AI / agents / memory / reshuffling), and a weekly calendar UI.

**Non-goals for Phase 1:** multi-agent systems, LLM calls (including LangChain/LangGraph), long-term memory, automatic reshuffling, Google Calendar write-back, mobile apps, recurring-event logic beyond minimal import of instances returned by the Google API.

---

## 1) What Already Exists (Relevant Files)

| Area | Path | Role today |
|------|------|------------|
| Monorepo docs | `README.md` | Run instructions, UUID + timezone standards |
| Compose | `docker-compose.yml` | Postgres, Redis, `api`, `worker`, `web`; dev bind mounts; health gating |
| Root env template | `.env.example` | Postgres credentials for Compose |
| Python tooling | `pyproject.toml` | Black / Ruff / Mypy targets for Python 3.11 |
| API entry | `apps/api/app/main.py` | FastAPI app, Sentry init, includes health router |
| API config | `apps/api/app/config.py` | `ENVIRONMENT`, `DATABASE_URL`, `SENTRY_DSN` via `pydantic` + `dotenv` |
| API DB helper | `apps/api/app/database.py` | SQLAlchemy engine + `SELECT 1` readiness |
| API health | `apps/api/app/health.py` | `GET /health`, `GET /ready` |
| API time helpers | `apps/api/app/utils/time.py` | `utc_now()`, `to_user_timezone()` — align Phase 1 datetime handling with this |
| API IDs | `apps/api/app/utils/uuid.py` | UUID v4 helper(s) — align entity IDs with repo standard |
| API deps | `apps/api/requirements.txt` | FastAPI, SQLAlchemy, psycopg2, pydantic, uvicorn, Sentry, lint/type tools |
| API container | `apps/api/Dockerfile` | Python 3.11, uvicorn `--reload` |
| Worker | `apps/worker/worker/celery_app.py`, `tasks.py` | Celery + Redis broker; example task only |
| Worker deps | `apps/worker/requirements.txt` | celery, redis, dotenv |
| Web app shell | `apps/web/app/layout.tsx`, `page.tsx` | Default Next layout + placeholder home |
| Web config | `apps/web/next.config.ts` | React Compiler enabled |
| Web deps | `apps/web/package.json` | Next 16, React 19, Sentry Next SDK |
| Web observability | `apps/web/sentry.*.config.ts` | Client / server / edge Sentry wiring |
| Web env template | `apps/web/.env.example` | `NEXT_PUBLIC_API_URL`, Sentry DSN vars |

**Not present today (README mentions future layout):** `packages/*`, `infra/docker` — Phase 1 can proceed without them; add shared types later if duplication hurts.

---

## 2) Phase 1 Product Scope (Locked)

1. **Auth + onboarding** — Google sign-in via **Auth.js** (NextAuth successor) on the web app; persist user profile; collect **working hours** and **preferred deep work windows** (interpreted in the user’s IANA timezone).
2. **Google Calendar (read-only)** — ingest events for scheduling context; classify **busy** vs **free**; no write-back.
3. **Task inbox** — CRUD for tasks with: **title**, **duration (minutes)**, **deadline** (instant in time, stored UTC), **priority** (enumerated).
4. **Deterministic scheduler** — no optimization solver: **greedy sequential placement** into free time; **deep work** vs **mechanical** split; chunking rules below.
5. **Weekly calendar** — show imported Google busy blocks + generated Chronos sessions for a selected week.

---

## 3) Proposed Backend Architecture Additions (`apps/api`)

Organize by **feature modules** (not a single `routes.py`). Suggested layout:

```text
apps/api/app/
  core/                 # shared: security, time, pagination errors
  db/
    session.py          # SessionLocal, dependency get_db
    base.py             # declarative Base
  models/               # SQLAlchemy models (thin)
  schemas/              # Pydantic request/response DTOs (strict)
  features/
    users/
      router.py
      service.py
      repository.py
    tasks/
      ...
    calendar_google/
      client.py         # thin wrapper around Google API calls
      sync_service.py
      repository.py
      router.py
    scheduling/
      engine.py         # pure deterministic algorithm + types
      service.py        # load inputs, persist outputs
      router.py
  migrations/           # Alembic (recommended) — versioned DDL
```

### 3.1 Configuration (new env vars)

Extend `Settings` (`apps/api/app/config.py`) with typed fields, for example:

- **Auth / API security:** `AUTH_JWT_SECRET` (or public JWKS URL if you later split issuers), `AUTH_JWT_ISSUER`, `AUTH_JWT_AUDIENCE` (tunable claims), optional `INTERNAL_CRON_SECRET` if you add admin-only sync triggers.
- **Google Calendar:** `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REDIRECT_URI` (if any server-side OAuth exchange is used).
- **Encryption:** `TOKEN_ENCRYPTION_KEY` (32-byte material for Fernet/AES-GCM — store refresh tokens encrypted at rest).

Keep **UTC at rest**; accept/return ISO-8601 with explicit offsets or Z; apply user TZ only in transformation layers when needed (UI primarily).

### 3.2 Authentication model (recommended)

**Auth.js on `apps/web`** performs Google OAuth for user identity.

**FastAPI** protects business endpoints by validating a **JWT** minted by Auth.js (JWT session strategy) *or* by accepting a dedicated **API access token** issued by a small Next server route after Auth.js session is established.

**Recommendation for Phase 1 clarity:** Auth.js **JWT sessions** using a shared secret (`AUTH_SECRET`) also known to FastAPI; FastAPI validates signature + standard claims (`exp`, `iss`, `sub`). The `sub` claim should map to **`users.id`** (UUID) in Postgres (not Google’s subject directly), created on first login.

Alternative (also valid): opaque session in DB via Auth.js adapter in Next + **BFF**: Next server calls FastAPI with `Authorization: Bearer <server-minted token>` per request. This adds token minting code in Next but avoids coupling JWT formats.

The plan assumes **JWT validated in FastAPI** unless implementation discovers Auth.js constraints that favor the BFF token approach.

### 3.3 Google Calendar token handling

- Request offline access once (`access_type=offline`, `prompt=consent` on first connect) to obtain a **refresh token**.
- Store **encrypted refresh token** per user in Postgres.
- Use Celery for **periodic sync** + manual “Sync now” endpoint.

### 3.4 Workers

Add Celery tasks in `apps/worker`:

- `calendar.sync_user(user_id)` — pull events for a bounded window (e.g., current week ± buffer).
- Optional: `schedule.regenerate_user_week(user_id, week_start_local_date)` if regeneration is async; Phase 1 can remain synchronous in API if fast enough for MVP.

---

## 4) Proposed Frontend Architecture Additions (`apps/web`)

### 4.1 Dependencies to add (Phase 1)

- **Auth.js** (`next-auth` v5 compatible packages for Next 16 — pin per official docs at implementation time).
- **HTTP client** for browser (optional): native `fetch` wrappers are fine.
- **Calendar UI**: start with custom grid (no heavy deps) or a small headless date lib if needed (`date-fns` / `@internationalized/date` — decide during implementation; avoid bringing large calendar suites unless necessary).

### 4.2 Route & layout structure

Use route groups for clarity:

```text
app/
  (marketing)/             # optional: public landing
  (auth)/
    login/page.tsx
  onboarding/
    page.tsx               # working hours + deep work prefs
  (app)/                   # authenticated shell
    layout.tsx             # nav + session guard
    inbox/page.tsx
    calendar/week/page.tsx
  api/auth/[...nextauth]/route.ts # Auth.js handler (path per library version)
```

**Session guard:** server-first (`getServerSession` equivalent) redirect unauthenticated users from `(app)` routes to `/login`.

### 4.3 Data fetching pattern

- Prefer **Server Components** for initial loads where simple; use **server actions** or route handlers to call FastAPI with the user’s token.
- Keep timezone conversion **in the UI** when rendering local week grids; send UTC instants to API.

### 4.4 Env templates

Update `apps/web/.env.example` with Auth.js + Google OAuth client settings (`AUTH_SECRET`, `AUTH_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, etc. — exact keys per Auth.js v5 docs).

---

## 5) Database Schema (Phase 1)

All primary keys: **UUID v4** (`users.id`, etc.). All timestamps: **`timestamptz` stored in UTC**.

### 5.1 `users`

| Column | Type | Notes |
|--------|------|--------|
| `id` | UUID PK | Canonical user id; maps to JWT `sub` |
| `email` | text, unique | From Google |
| `google_sub` | text, unique | Stable Google subject |
| `full_name` | text, nullable | Profile |
| `timezone` | text | IANA, e.g. `America/Los_Angeles` |
| `working_hours` | jsonb | Structured weekly availability (see below) |
| `deep_work_preferences` | jsonb | Preferred windows (see below) |
| `onboarding_completed_at` | timestamptz, nullable | Null until finished |
| `created_at` / `updated_at` | timestamptz | Audit |

**`working_hours` JSON shape (example):**

```json
{
  "week": {
    "mon": [{"start": "09:00", "end": "17:00"}],
    "tue": [{"start": "09:00", "end": "17:00"}]
  }
}
```

**`deep_work_preferences` JSON shape (example):**

```json
{
  "week": {
    "mon": [{"start": "08:00", "end": "12:00"}],
    "wed": [{"start": "13:00", "end": "16:00"}]
  }
}
```

Store *local* wall-clock times paired with `users.timezone`; normalize to UTC when computing schedules for a concrete week.

### 5.2 `oauth_accounts` (or `user_oauth_tokens`)

| Column | Type | Notes |
|--------|------|--------|
| `user_id` | UUID FK | |
| `provider` | text | `google` |
| `refresh_token_ciphertext` | bytea/text | Encrypted |
| `scopes` | text | Space-separated |
| `token_updated_at` | timestamptz | |

### 5.3 `calendar_events` (imported, read-only)

| Column | Type | Notes |
|--------|------|--------|
| `id` | UUID PK | |
| `user_id` | UUID FK | |
| `provider` | text | `google` |
| `external_id` | text | Google event id; unique per user |
| `start_at` / `end_at` | timestamptz | UTC |
| `summary` | text, nullable | |
| `status` | text | `confirmed` / `tentative` / `cancelled` |
| `transparency` | text, nullable | Map `opaque` → busy, `transparent` → free when applicable |
| `is_busy` | boolean | Derived: default busy if opaque or unknown; respect all-day rules |
| `updated_at_provider` | timestamptz, nullable | If available |
| `raw_payload` | jsonb, nullable | Optional debugging; can omit in prod later |

**Minimal recurring handling:** store each **instance** Google returns in the queried time window; do not expand RRULE yourself in Phase 1.

### 5.4 `tasks`

| Column | Type | Notes |
|--------|------|--------|
| `id` | UUID PK | |
| `user_id` | UUID FK | |
| `title` | text | |
| `duration_minutes` | int | >0 |
| `deadline` | timestamptz | UTC instant |
| `priority` | enum/text | e.g. `P1` highest → `P4` lowest (define fixed set) |
| `created_at` / `updated_at` | timestamptz | |

### 5.5 `scheduled_sessions` (Chronos-generated)

| Column | Type | Notes |
|--------|------|--------|
| `id` | UUID PK | |
| `user_id` | UUID FK | |
| `task_id` | UUID FK | |
| `start_at` / `end_at` | timestamptz | UTC; `end - start` equals session duration |
| `session_kind` | text | `deep_work` \| `mechanical` |
| `chunk_index` | int | 0-based; mechanical tasks use `0`; deep chunks increment |
| `week_start_date` | date | User-local week key for idempotent replace (see algorithm) |

**Idempotency:** regenerating a week should **delete + recreate** rows for `(user_id, week_start_date)` in one transaction.

---

## 6) API Endpoints (Phase 1)

All JSON APIs are **authenticated** unless noted.

### 6.1 Auth bootstrap

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/users/me` | Current user profile + onboarding flags |
| `PATCH` | `/users/me` | Update timezone, working hours, deep work prefs; set onboarding complete |

### 6.2 Google Calendar

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/integrations/google/connect` | Begin OAuth token capture if using backend flow; **or** this becomes a token exchange endpoint if Auth.js supplies tokens — choose one coherent flow during implementation |
| `POST` | `/calendar/sync` | Trigger sync now for default window |
| `GET` | `/calendar/events` | Query params: `from`, `to` (UTC ISO) — returns imported events |

### 6.3 Tasks

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/tasks` | Create |
| `GET` | `/tasks` | List (filter: `status` optional later; Phase 1 can be all active) |
| `GET` | `/tasks/{task_id}` | Detail |
| `PATCH` | `/tasks/{task_id}` | Update |
| `DELETE` | `/tasks/{task_id}` | Delete |

### 6.4 Scheduling

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/schedule/week` | Body: `week_start` (user-local date), optional flags; runs deterministic scheduler for that week |
| `GET` | `/schedule/sessions` | Query: `from`, `to` — returns generated sessions |

**Existing endpoints remain:** `GET /health`, `GET /ready`.

---

## 7) Web App Routes / Pages (Phase 1)

| Route | Purpose |
|-------|---------|
| `/login` | Google sign-in entry |
| `/onboarding` | Working hours + deep work preferences + timezone confirmation |
| `/inbox` (under `(app)/`) | Task list + create/edit |
| `/calendar/week` | Weekly grid: Google busy + Chronos sessions |

**Global:** `(app)/layout.tsx` provides navigation + auth gate.

---

## 8) Deterministic Scheduler — Design

### 8.1 Definitions

- **Working availability:** for each local day in the target week, take user `working_hours` intervals.
- **Busy blocks:** union of imported Google events classified as **busy** within the week window.
- **Free intervals:** `availability - busy` per day, merged for contiguous gaps (in UTC after conversion).
- **Task classes:**
  - **Deep work task:** `duration_minutes > 60` → `session_kind = deep_work`.
  - **Mechanical task:** `duration_minutes <= 60` → `session_kind = mechanical`.

### 8.2 Deep work chunking

For deep work tasks, split into chunks:

- All chunks **≤ 45 minutes** except allow the final remainder **< 45** as the last chunk.
- Example: 120 → 45 + 45 + 30; 70 → 45 + 25.

Mechanical tasks: **single session** of exactly `duration_minutes` (no splitting).

### 8.3 Ordering (deterministic, global)

Sort tasks before placement:

1. **Priority** ascending (P1 before P2 — define numeric mapping internally).
2. **Deadline** ascending (earlier first).
3. **Created_at** ascending (older first — stable tie-break).
4. **Task id** lexicographic (ultimate stability).

For deep tasks, sort **chunks** by `(parent task order, chunk_index)`.

### 8.4 Placement algorithm (greedy)

For each unit of length `L`:

1. Scan free intervals left-to-right.
2. Find the first interval where `(end - start) >= L`.
3. Place session at `[start, start+L)`.
4. Shrink that free interval to `[start+L, end)`.
5. If interval empty, remove it.

If no interval fits, **skip** the unit (MVP behavior) and continue; collect **unplaced** items for API response diagnostics (`unplaced_task_ids`).

**Inputs (summary):**

- Ordered list of **work units** (mechanical task = 1 unit; deep task = N chunks).
- List of **free intervals** `[start, end)` in UTC, sorted by start, non-overlapping.

**Optional MVP refinement (if skipping is too harsh):** allow mechanical tasks to be placed in the **first** slot that fits after sorting tasks — still deterministic; document chosen rule in API response.

### 8.5 Week boundary

- Accept `week_start` as a **user-local calendar date** (Monday 00:00 local recommended; document assumption in API).
- Compute `week_end` as +7 days.
- Clip sessions so they do not exceed the `[week_start, week_end)` window (tasks should not span outside for Phase 1; if a chunk would cross boundary, treat as **unplaced**).

### 8.6 DST / timezone

- Always convert working hours + week boundaries using `zoneinfo` on the API to avoid ambiguous local times; reject or adjust ambiguous instants explicitly (document behavior).

---

## 9) Implementation Order & Milestones

### Milestone A — Data layer & tooling

- Add Alembic + initial migration for tables above.
- Add `get_db` dependency, transaction boundaries, repository pattern per feature.

**Exit criteria:** migrations apply cleanly against Compose Postgres; `/ready` still works.

### Milestone B — Auth end-to-end

- Auth.js Google login on web; create `users` row on first login; JWT validation on FastAPI protected routes.

**Exit criteria:** calling `/users/me` returns profile for logged-in user; unauthenticated returns 401.

### Milestone C — Onboarding

- UI + API for timezone, `working_hours`, `deep_work_preferences`, `onboarding_completed_at`.

**Exit criteria:** new user cannot access `(app)` until onboarding complete (or soft-gate with banner — pick one; recommend hard gate).

### Milestone D — Google Calendar read sync

- Encrypted refresh token storage; Celery sync task; `calendar_events` populated; `GET /calendar/events`.

**Exit criteria:** weekly view can render imported busy events from DB.

### Milestone E — Task inbox

- Full CRUD + validation (duration > 0, deadline required, priority enum).

**Exit criteria:** tasks persist; list stable ordering documented.

### Milestone F — Scheduler + sessions API

- Implement `engine.py` pure function with golden tests; `POST /schedule/week` replaces sessions for that week.

**Exit criteria:** deterministic output for fixed inputs; documented unplaced behavior.

### Milestone G — Weekly calendar UI

- Combine Google events + sessions; local TZ display.

**Exit criteria:** user can step weeks and see combined grid.

### Milestone H — Hardening

- Rate limits (optional), structured logging, minimal audit fields, Sentry breadcrumbs for sync failures.

---

## 10) Risks & Edge Cases

| Risk | Mitigation |
|------|------------|
| Auth.js ↔ FastAPI JWT coupling | Prefer documented JWT session config; integration test token validation; fallback BFF token design |
| Google refresh token not issued | Force `prompt=consent` on first connect; surface clear UI error |
| Token encryption key mishandled | Load from env; fail fast if missing in prod |
| All-day events | Treat as busy full local day; convert to UTC carefully |
| `transparent` vs `opaque` | Map to free vs busy; default conservative (busy) when unknown |
| DST gaps/folds | Use `zoneinfo`; test America/* and Europe/* zones |
| Long tasks exceed weekly free time | Expect `unplaced` list; show in UI |
| Deep chunks fragment calendar | Accept MVP UX; no AI reshuffle in Phase 1 |
| Redis/worker outage | Sync can fail softly; expose last sync timestamp + error |
| SQL injection / bad input | Pydantic strict schemas; parameterized queries |

---

## 11) Testing Strategy

### 11.1 Backend (pytest)

- **Unit tests:** `scheduling/engine.py` with fixed clocks, fixed timezones, fixed busy blocks — snapshot expected placements.
- **Repository tests:** optional with ephemeral Postgres (Testcontainers or CI service).
- **API tests:** `TestClient` for auth dependency overridden + CRUD happy paths and validation errors.

### 11.2 Frontend

- **Component tests** (optional Phase 1): weekly grid edge rendering with mocked data.
- **E2E** (Playwright — add when worthwhile): login smoke test in staging only (Google OAuth is awkward locally — use test account or mock).

### 11.3 Tooling

- Keep **Ruff / Black / Mypy** on CI for Python; **ESLint / Prettier / `tsc --noEmit`** for web once auth code lands.

---

## 12) Open Decisions (Resolve During Implementation, Not Scope Creep)

- Exact **priority enum** labels and sort mapping.
- Whether **regeneration** deletes manual edits (N/A in Phase 1 if sessions are system-only).
- Whether to show **unplaced tasks** prominently or as a secondary panel.

---

**Document owner:** Engineering  
**Status:** Plan only — implementation follows milestones above.
