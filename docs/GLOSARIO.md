# VerduPrecios — Domain Glossary

> Terms from the verdulería / Mercado Central world and how this project uses them.
> Product/domain terms keep their Argentine Spanish form; definitions are in English.

## Products

- **Producto (product)** — the canonical fruit or vegetable (papa, banana, tomate). This is the level of comparison.
- **Variedad (variety)** — the named variant of a product (papa *agata*, papa *spunta*). Aggregates up to product level.
- **Origen (origin)** — where the produce comes from (BRASIL, CATAMARCA…).
- **Categoría (category)** — **fruta** (fruit) or **verdura** (vegetable).

## Units & packaging

- **Envase / envasado (packaging)** — how it's sold: bolsa (bag), atado (bunch), caja (box)…
- **Peso del envase (package weight, kg)** — e.g. a 25 kg or 18 kg bag. Crucial to convert to **price per kg**.
- **Precio por kg (price per kg)** — the common unit of comparison across products with different package weights.

## The price data

- **Calidad (quality grade)** — commercial grade: **1A**, **2A** (refined vs coarser).
- **Tamaño (size)** — MEDIANO, GRANDE… (the product's caliber).
- **Precio mín / típico / máx (min / typical / max price)** — the wholesale reference is a range, not a single value.
- **Variación semanal (weekly change)** — how the price moved vs the previous week.

## Project concepts

- **Temporada (season)** — when a product is in its natural season in Argentina.
  Base: a fixed calendar; supporting signal: the price (climate can distort it).
- **Mercado Central (MC)** — Buenos Aires' wholesale market; our price reference.
- **Verdulería (greengrocer)** — the neighborhood produce store. Today only a future vision (community input).
- **Fixture** — a hand-captured data sample (e.g. a copy of the MC price page HTML) used as test
  input with no network required.
- **Modular monolith** — one app with strict layer separation (`routers → services → models → db`);
  dependencies flow in one direction. No microservices.
- **Price observation (event)** — a single timestamped price reading; stored as **append-only history**,
  never overwritten.
- **Migration (Alembic)** — a versioned schema change applied to PostgreSQL, recorded in the migration history.

## Working-process terms

- **MVP** — the minimum version: extract MC prices and show cheapest / most expensive / in-season.
- **Commit per day** — the working rhythm: one 30-minute commit per day.
- **TDD** — write the failing test first, then the logic that makes it pass.
