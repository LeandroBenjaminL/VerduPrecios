# 🥬 VerduPrecios

> Real-time fruit & vegetable price tracking from Buenos Aires' **Mercado Central**
> (wholesale market). Built as a **modular monolith** — deliberately written by hand, decision by decision.

**Status: Data Core phase (Fase 1)** — SQLAlchemy models + Alembic migrations. No API yet.
**Stack:** Python · FastAPI · Pydantic · PostgreSQL · SQLAlchemy 2.0 · Alembic

## What it answers

1. **What's cheapest?** — ranking by price per kg
2. **What's most expensive?** — the other end of the ranking
3. **What's in season?** — season calendar + price as supporting signal

## How it works (the domain pipeline)

```
Mercado Central price data (HTML)        Phase 2: Ingest
        │
        ▼
Structured records → PostgreSQL          Phase 1: Data core (models + migrations)
        │
        ▼
Services: normalize to price/kg, rank,   Phase 3: Service layer
season logic (calendar + price signal)
        │
        ▼
FastAPI endpoints                        Phase 4: API
```

## Architecture

A **modular monolith**: strict layer separation inside one app —
`routers → services → models → db`, dependencies flow in **one direction only**.
Zero microservices: MVP-scale discipline without the ops complexity.

Core design rule: prices are modeled as **timestamped events** (append-only history),
never as an overwritten "current price". That's what makes rankings, trends and
season logic queries instead of re-engineering.

## Roadmap (current)

| Phase | Content |
| :---- | :------ |
| 1 | **Data core** — models + initial Alembic migrations |
| 2 | Ingest — parse Mercado Central price data into the DB |
| 3 | Services — normalize to price/kg, rank, season logic |
| 4 | API — FastAPI endpoints exposing results |
| 5+ | Future: community registry (users, verdulerías, reviews) |

## Pending design decisions (Phase 1)

- Ingest as a later phase feeding the DB, or models-only first? → **to be decided**
- Full catalog (product + variety + season) or minimal cut for the first migration? → **to be decided**
- Prices are modeled as **timestamped events** (append-only history), not overwritten values.

## Vision (future direction — not built)

The eventual product is a **community price registry**: users log prices at their
greengrocers (verdulerías), stores are created and visible to everyone, and
feedback/reviews shape trust. None of this is implemented yet — Phase 1 is the data core.

## Live data source (for the ingest phase)

- **Mercado Central — Precios Mayoristas** (weekly price tables, HTML):
  <https://mercadocentral.gob.ar/información/precios-mayoristas>
- Monthly ZIP archives of price lists — a candidate source for the ingest phase later.
