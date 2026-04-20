# 🧠 Chronos Database Design (MVP - Separate Tables Model)

---

## 📌 Primary Decision

### **Primary Modeling Approach: Separate Time Tables**

Chronos uses a **relational scheduling model** where fixed commitments and generated work sessions are stored in **separate tables**.

- `calendar_events` stores fixed or synced commitments
- `schedule_sessions` stores generated Chronos work blocks

---

## 🎯 Purpose

This model separates two fundamentally different kinds of time data:

| Data Type         | Stored In            | Examples                          |
|------------------|----------------------|-----------------------------------|
| Fixed Events      | `calendar_events`    | Classes, meetings, work shifts    |
| Work Sessions     | `schedule_sessions`  | Coding, studying, writing blocks  |

This keeps the schema cleaner and easier to reason about.

---

## 🔀 Differentiation Strategy

Instead of one polymorphic table, Chronos separates time data by lifecycle and purpose:

| Table                | Role |
|---------------------|------|
| `calendar_events`    | External synced fixed commitments |
| `schedule_sessions`  | Internal generated work sessions |

---

## 🚀 Why This Works Better for Chronos

Chronos needs a scheduling engine that is:

- Reliable  
- Maintainable  
- Easy to debug  
- Safe for production  
- Expandable for future AI features  

Using separate tables enables:

- Clearer domain boundaries  
- Easier sync logic for Google Calendar  
- Easier execution tracking for user work sessions  
- Cleaner validation rules  
- Better long-term maintainability  

---

## ⚠️ Important Design Rule

### **TimeBlock remains a domain concept, not a persisted table**

Chronos still thinks in terms of “time blocks” at the product and scheduling-engine level, but in the database:

- Fixed commitments live in `calendar_events`
- Generated work chunks live in `schedule_sessions`

This gives you the conceptual benefits of TimeBlock without the schema complexity of a single overloaded table.

---

## 🧱 Core Tables (MVP)

| Table Name             | Purpose |
|-----------------------|--------|
| `users`               | User identity |
| `user_preferences`    | Scheduling preferences |
| `connected_calendars` | Google Calendar connection metadata |
| `calendar_events`     | Synced fixed commitments |
| `tasks`               | User-defined work items |
| `schedules`           | Weekly schedule containers |
| `schedule_sessions`   | Scheduled work blocks |
| `session_logs`        | Session activity and completion history |

---

## 🧩 What `calendar_events` Represents

Each row in `calendar_events` represents a **fixed or externally synced time block**.

### Examples
- Class
- Office meeting
- Work shift
- Recurring event from Google Calendar

### Responsibilities
- Reflect external commitments
- Support sync and deduplication
- Preserve source metadata

---

## 🧩 What `schedule_sessions` Represents

Each row in `schedule_sessions` represents a **generated Chronos work session**.

### Examples
- Coding session
- Study block
- Writing session
- Future break or buffer block if needed

### Responsibilities
- Represent scheduled work
- Track completion state
- Support replanning and analytics

---

## 🗂️ `calendar_events` Schema (High-Level)

| Field                | Description |
|---------------------|-------------|
| `id`                | UUID primary key |
| `user_id`           | Owner |
| `connected_calendar_id` | Source calendar |
| `external_event_id` | External provider event ID |
| `title`             | Event title |
| `description`       | Optional description |
| `location`          | Optional location |
| `start_at`          | Start timestamp (UTC) |
| `end_at`            | End timestamp (UTC) |
| `is_all_day`        | Boolean |
| `is_recurring`      | Boolean |
| `recurrence_rule`   | Optional recurrence data |
| `status`            | External/sync event state |
| `is_busy`           | Whether the event blocks scheduling |
| `raw_payload`       | JSONB external provider data |
| `last_synced_at`    | Last sync timestamp |
| `created_at`        | Timestamp |
| `updated_at`        | Timestamp |

---

## 🗂️ `schedule_sessions` Schema (High-Level)

| Field                     | Description |
|--------------------------|-------------|
| `id`                     | UUID primary key |
| `schedule_id`            | Parent weekly schedule |
| `user_id`                | Owner |
| `task_id`                | Linked task (nullable if future non-task session type) |
| `session_type`           | Session category |
| `title`                  | Display title |
| `planned_start_at`       | Planned start timestamp (UTC) |
| `planned_end_at`         | Planned end timestamp (UTC) |
| `planned_duration_minutes` | Planned duration |
| `actual_start_at`        | Actual execution start |
| `actual_end_at`          | Actual execution end |
| `actual_duration_minutes` | Actual duration |
| `status`                 | Session execution state |
| `source`                 | Creation source |
| `position_index`         | Order within generated schedule |
| `created_at`             | Timestamp |
| `updated_at`             | Timestamp |

---

## ⚙️ Type / Session Classification Rules

### `calendar_events`
Stores only externally sourced or synced commitments.

Must support:
- sync metadata
- recurrence metadata
- external provider IDs
- raw provider payload

---

### `schedule_sessions`
Stores only Chronos-generated or manually adjusted work sessions.

Must support:
- task linkage
- schedule linkage
- completion/missed tracking
- actual duration tracking

---

## 🧠 Design Philosophy

**TimeBlock is an internal abstraction, not a database table.**

Chronos treats time as the **primary resource**, but persists different classes of time separately based on their operational behavior.

This gives the system:

- conceptual clarity  
- database cleanliness  
- safer future evolution  

---

## 🔄 Scheduling Flow (MVP)

1. Read user preferences
2. Read active tasks
3. Read synced fixed events from `calendar_events`
4. Compute free time windows in memory
5. Generate a new schedule record in `schedules`
6. Insert generated work blocks into `schedule_sessions`

---

## ⏱️ Time Strategy

- Store all timestamps in **UTC**
- Convert to user timezone in frontend
- Store user timezone in `users.timezone`

This is required for calendar correctness.

---

## 🧩 Key Enums

### Task Priority
- `low`
- `medium`
- `high`
- `urgent`

### Task Type
- `deep`
- `mechanical`
- `unspecified`

### Task Status
- `inbox`
- `scheduled`
- `in_progress`
- `completed`
- `deferred`
- `cancelled`

### Schedule Generation Type
- `initial`
- `manual_replan`
- `auto_replan`

### Schedule Status
- `draft`
- `active`
- `replaced`
- `archived`

### Session Type
- `deep_work`
- `mechanical`
- `buffer`
- `break`

### Session Status
- `planned`
- `completed`
- `missed`
- `skipped`
- `partial`
- `cancelled`

### Classification Source
- `manual`
- `ai`
- `rule`

### Session Source
- `rule_engine`
- `ai_assisted`
- `manual`

---

## 🧠 AI / Future Readiness

This design supports future AI and LLM integration without forcing AI into the MVP core.

### Future-friendly fields already planned
- `tasks.classification_source`
- `calendar_events.raw_payload`
- future summary payload fields
- optional audit metadata

### Future tables that can be added later
- `agent_runs`
- `task_classification_history`
- `schedule_generation_runs`
- `user_behavior_patterns`
- `notification_events`

---

## 📈 Indexing Strategy

| Table                | Index |
|---------------------|------|
| `users`             | `unique(email)` |
| `calendar_events`   | `(user_id, start_at)` |
| `calendar_events`   | `(user_id, end_at)` |
| `calendar_events`   | `unique(connected_calendar_id, external_event_id)` |
| `tasks`             | `(user_id, status)` |
| `tasks`             | `(user_id, deadline_at)` |
| `tasks`             | `(user_id, priority)` |
| `schedules`         | `(user_id, week_start_date)` |
| `schedules`         | `(user_id, status)` |
| `schedule_sessions` | `(schedule_id)` |
| `schedule_sessions` | `(user_id, planned_start_at)` |
| `schedule_sessions` | `(user_id, status)` |
| `schedule_sessions` | `(task_id)` |
| `session_logs`      | `(session_id, logged_at)` |

---

## 🧼 Data Integrity Rules

### General
- `end_at > start_at`
- all planned durations must be positive
- actual durations must be non-negative
- all datetime values stored in UTC

### `calendar_events`
- `end_at > start_at`
- `external_event_id` should be unique per connected calendar

### `tasks`
- `estimated_minutes > 0`

### `schedule_sessions`
- `planned_end_at > planned_start_at`
- `planned_duration_minutes > 0`
- actual times nullable unless started

### `schedules`
- `week_end_date >= week_start_date`

---

## 🗑️ Deletion Strategy

| Entity                 | Strategy |
|-----------------------|----------|
| `tasks`               | Soft delete via `archived_at` |
| `calendar_events`     | Hard delete and re-sync safe |
| `schedule_sessions`   | Hard delete when replacing schedule versions |
| `connected_calendars` | Disable sync instead of deleting immediately |

Do not soft-delete everything by default. That creates unnecessary query complexity.

---

## 🧭 Final Summary

- **Database:** PostgreSQL
- **Modeling Style:** Relational SQL schema with separate time tables
- **Architecture:** Modular monolith
- **Time Handling:** UTC-based storage with user timezone conversion
- **Core Scheduling Rule:** TimeBlock is an internal abstraction only

### Core Tables
- `users`
- `user_preferences`
- `connected_calendars`
- `calendar_events`
- `tasks`
- `schedules`
- `schedule_sessions`
- `session_logs`

### Optional Near-Term
- `weekly_summaries`

### Key Modeling Rule
- fixed commitments are stored in `calendar_events`
- generated work chunks are stored in `schedule_sessions`

---

## 🧱 Core Principle

Chronos is not just a task manager.  
It is a **time allocation and scheduling engine** built on a clean separation between external commitments and internally generated work sessions.
