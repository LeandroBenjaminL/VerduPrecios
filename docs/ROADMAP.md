# VerduPrecios — Roadmap

> The plan and the **next steps**. Each phase = your implementation, in daily commits.
> Log your progress in [`PROGRESO.md`](PROGRESO.md); design details live in [`DESIGN.md`](DESIGN.md).

## Phases

| Phase | Content | Done when |
| :---- | :------ | :-------- |
| **1 — Data Core** | SQLAlchemy models (Product, Variety, PriceObservation, SeasonCalendar) + initial Alembic migration. With tests. | Schema applies cleanly; migration is versioned; models validated by tests. |
| **2 — Ingest** | Parse Mercado Central price data (HTML) into structured records → load into PostgreSQL via the models. | Real MC data lands in the DB through the models, tested. |
| **3 — Services** | Normalize to price per kg; aggregate varieties to product level; cheapest / most-expensive ranking + in-season logic (calendar + price signal). | Correct answers, fully tested. |
| **4 — API** | FastAPI endpoints exposing the results (and price history). | HTTP endpoints return the data. |
| **5 — Community (future)** | Users log prices, open verdulerías, feedback/reviews. | The vision — much later. |

## Now: the next step is Phase 1 — Data Core

The first thing to build is the **data core**: the SQLAlchemy models and the first
Alembic migration. This is where the project learns to stand on its own — hand-typed,
decision by decision.

### What Phase 1 contains

- **Product**: canonical fruit/vegetable, name + category (fruta / verdura). Maybe aliases for normalizing names later.
- **Variety**: named variant of a product (papa *agata*, papa *spunta*) — aggregates up to product level.
- **PriceObservation**: a single timestamped price reading (product + variety, origin, quality 1A/2A,
  size, package/unit, price range min/típico/max, date, source). Append-only history, never overwritten.
- **SeasonCalendar**: product → the months it's in season in Argentina.

### Suggested first sub-step (Day 1)

Start even smaller: just the **Product** model with its **category**, a couple of tests
(write the failing test first — that's TDD), and the **first Alembic migration**
running end to end against PostgreSQL.

### Things to decide as you go (note them here)

- Full catalog vs **minimal cut** for the first migration — you decide the set.
- How to represent the MC price range (min / typical / max) in the model.
- What counts as a "product" vs a "variety" for the first cut.
- Ingest (HTML parser) as a later phase, or models-only until further notice.

---
> Update this file's **Next steps** section below after each phase is done.

## Next steps (living list)

- [ ] Phase 1 — data core: models + first migration + tests
- [ ] Phase 2 — ingest: parse MC price data into the DB
- [ ] Phase 3 — services: normalize, rank + season logic
- [ ] Phase 4 — API: FastAPI endpoints
- [ ] (future) Phase 5 — community features
