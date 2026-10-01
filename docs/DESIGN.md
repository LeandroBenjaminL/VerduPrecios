# VerduPrecios — Design

> The single source of truth for **how** VerduPrecios works.
> Companion docs: [`ROADMAP.md`](ROADMAP.md) (plan & next steps), [`PROGRESO.md`](PROGRESO.md) (day-by-day log), [`GLOSARIO.md`](GLOSARIO.md) (domain terms).

## 1. What it is

A tool to see the **cheapest, most expensive, and in-season** fruit & vegetable prices
from Buenos Aires' **Mercado Central** (wholesale market).

One-line product story:

> *"¿Qué está barato, qué está caro y qué está de temporada en el Mercado Central?"*

## 2. MVP — plan (modular monolith, data first)

The MVP is a **real-time price tracking app** built as a **modular monolith**:
one app, strict layer separation, dependencies flowing in one direction
(`routers → services → models → db`). Zero microservices.

```
Mercado Central price data (HTML)   Phase 2: Ingest
   → Structured records → PostgreSQL
   → Services: normalize to price/kg, rank, season logic   Phase 3
   → FastAPI endpoints exposing results                    Phase 4
```

**Phase 1 is the data core**: SQLAlchemy models + initial Alembic migrations.
Everything grows from there: ingest (Phase 2), services (Phase 3), API (Phase 4).

## 3. Decisions (agreed together)

| Decision | Choice | Why |
| :------- | :----- | :-- |
| MVP scope | Extract MC prices; show cheapest / most expensive / in-season | Small, real, plays to logic strength |
| Architecture | **Modular monolith**; layers `routers → services → models → db` | MVP-scale discipline without microservice ops complexity |
| Stack | Python, FastAPI, Pydantic, PostgreSQL, SQLAlchemy 2.0, Alembic | Modern backend stack (junior backend target) |
| Data input | **Ingest phase (later)** parses MC price data into the DB; Phase 1 is the data core | The database is the foundation; parsing feeds it |
| Output | Web/API in a later phase; Phase 1 = models + migrations | Keeps Phase 1 focused and debuggable |
| Comparison basis | **Price per kg** | Packages have different weights (25kg, 18kg…) |
| Ranking level | **Product level** (varieties aggregate: PAPA AGATA → papa) | Clear, user-friendly |
| "In season" | **Real season calendar (base) + price as supporting signal**; tolerate climate noise | A product can be expensive even in its own season |
| Price model | **Timestamped event** (append-only history), never an overwritten value | Rankings, trends and season become queries, not re-engineering |
| Scope guard | **No users/verdulerías** in Phase 1 (community registry is the later vision) | Don't model what has no real user yet |

## 4. Domain model (sketch — details emerge as you implement)

```
Product        — canonical fruit/vegetable: name (papa), category (fruta | verdura), aliases
Variety        — a named variant of a product (agata, spunta) — metadata at product level
Unit/package   — how it's sold (bolsa 25 kg, bolsa 18kg …) → drives price-per-kg conversion
PriceRecord    — product(+variety), origin, quality (1A/2A), size, date,
                 price range (min / typical / max), source
SeasonCalendar — product → months in season (Argentina)
```

### Season logic (the interesting part)

- **Base:** a fixed calendar per product (its real season in Argentina) — reliable and deterministic.
- **Signal:** the normalized price supports/reinforces the calendar.
- **Caveat:** climate can make a product expensive even in its own season — the logic must
  tolerate that noise without failing.

### How prices are stored (the core design rule)

A price is an **event with a timestamp** — an observation of the market at a point in time.
The data core keeps an **append-only history** of these observations: nothing is ever
overwritten. Rankings, trends and season logic become queries over that history.
Users and verdulerías (the community vision) are **out of scope** for the Phase 1 model.

## 5. Data sources

| Source | Content | Format | Use |
| :----- | :------ | :----- | :-- |
| Mercado Central — Precios Mayoristas | weekly wholesale table: product, variety, origin, package, kg, quality, size, min/típico/max, weekly change | HTML | Phase 1 fixture → parse |
| MC monthly ZIPs (`FRUTAS-MAYO-2026.zip`) | same data, monthly archive | zip | candidate scraping source (later) |

Phase 1 uses a **hand-captured fixture** of the MC page only.

Reference: <https://mercadocentral.gob.ar/información/precios-mayoristas>

## 6. Non-goals (current)

- No microservices — the modular monolith is the whole architecture.
- No community features (users, verdulerías, reviews) — see [`VISION` in README](../README.md).
- No live scraping in Phase 1; ingest is a later phase that feeds the DB.
- No real-time push/streaming — "real time" means current weekly data, not websockets.

## 7. Working rules

- **Docs are mine** (Gentleman); **implementation, tests, and commits are Leandro's.**
- **Learning-by-hand premise:** Leandro types every line; the assistant explains the why
  and unblocks with the minimal piece — it never dumps large code blocks.
- Every unit of work lands with its tests green.
- One commit per day, driven by Leandro.
- Record each work session in [`PROGRESO.md`](PROGRESO.md).
- **Versioning — Semantic Versioning (pre-1.0, `0.x`):** `MAJOR.MINOR.PATCH`; one tag per
  completed phase (`v0.1.0` Data Core, `v0.2.0` Ingest, …); `v1.0.0` only when the MVP is
  deployed and stable. Tags live on `main`.
- **Branching — GitHub Flow (simplified):** `main` is always stable and green (tests pass);
  short `feature/<name>` branches per work unit, merged back when the block is complete with
  tests green. No `develop`, release or hotfix branches until there is something to deploy.

## 8. Tooling

| Area | Decision | Notes |
| :--- | :------- | :---- |
| Python runtime | **3.14** (WSL) | Floor: `requires-python = ">=3.14"` in `pyproject.toml`; pin: `.python-version` (uv auto-downloads that version for new clones) |
| Env / packages | **uv** | Modern standard; replaces manual `venv` + `pip` |
| Lint + format | **ruff** | One binary: lint + format + import sort |
| Testing | **pytest** | Non-negotiable |
| CI | **GitHub Actions** — run `ruff` + `pytest` on every push/PR to `main` | Enabled once the remote repo exists; a quality gate, not DevOps |
| Database runner | **Docker Compose** (`compose.yaml` + `.env.example`; real `.env` in `.gitignore`) | Reproducible for anyone who clones the repo |
| Analysis focus | **pending** — no notebooks; candidates: dbt (SQL analytics) / typed analysis scripts / Streamlit | Decide before Phase 3 |
