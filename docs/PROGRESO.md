# VerduPrecios — Progress Log

> The day-by-day record ("registro perfecto"). Add an entry after each work session,
> one commit per day. Today's date goes at the top.

---

## 2026-10-01 — Phase 1a kickoff: uv tooling + first TDD cycle green (Product)

- **What:** Started Phase 1a (domain in pure Python, no DB/ORM yet — deliberate, to avoid splitting focus between domain and SQL in the first sessions). Set up uv tooling (pytest as dev dependency; `.venv` auto-created; interpreter later re-pinned to the installed 3.14 — see decision below). First hand-typed TDD cycle: wrote the failing test (`tests/test_product.py`), hit the real `sys.path` problem (project root not on pytest's module search path → `ModuleNotFoundError: No module named 'models'` even though the folder existed), fixed it with `[tool.pytest.ini_options] pythonpath = ["."]` in `pyproject.toml`, then implemented the minimal `Product` class and reached green.
- **Files:** `pyproject.toml`, `.python-version`, `tests/test_product.py`, `models/__init__.py`, `models/product.py` (+ auto-generated `.venv/`)
- **Decisions:** Phase 1 split — 1a: domain models in pure Python with tests; 1b (later): SQLAlchemy + PostgreSQL + Alembic. Domain terms: Product = the good (papas, manzanas), Variety = the named variant (papa agata, papa spunta); variety name is unique per product. Method agreement: Leandro writes all code himself; the assistant explains concepts and unblocks with the minimal piece only when stuck.
- **Decisions (runtime):** Use the installed interpreter (CPython 3.14) instead of the earlier 3.12 intent: `requires-python = ">=3.14"` (floor) + `.python-version` = `3.14` (pin; uv downloads it automatically for new clones). Reflected in DESIGN.md §8.
- **Tests:** `uv run pytest` → 1 passed (`test_product_holds_name_and_category`)
- **Next:** First repo commit (Leandro's call) — `.venv/` already gitignored, green test in place. Then: next TDD cycle growing `Product` coverage (e.g. rejects an unknown or empty category), then `Variety` (name unique per product).

---

## 2026-09-06 — Replan: modular monolith, git cleanup, docs updated

- **What:** Replanned the project with a new direction: real-time fruit & vegetable price tracking
  as a **modular monolith** (Python + FastAPI + Pydantic + PostgreSQL + SQLAlchemy 2.0 + Alembic).
  Phase 1 is now the **data core** (models + migrations). Removed an unrequested AI attempt:
  the repo had no commits, so the staged leftovers were cleaned (index reset, unreachable objects
  pruned — nothing of ours was lost). Updated README, DESIGN and ROADMAP to the new direction.
- **Files:** `README.md`, `docs/DESIGN.md`, `docs/ROADMAP.md`, `.gitignore` (+ private `.gentleman/`)
- **Decisions:** modular monolith (no microservices); layers flow `routers → services → models → db`;
  prices are **timestamped events** (append-only history); no users/verdulerías in Phase 1.
- **Tests:** none yet (docs only).
- **Next:** decide the Phase 1 cut (full catalog vs minimal; ingest as a later phase?) and build
  the first model + the first Alembic migration, hand-typed.

---

## 2026-09-01 — Project kickoff

- **What:** Defined the project (VerduPrecios), repo created, README + docs written.
- **Files:** `README.md`, `docs/DESIGN.md`, `docs/ROADMAP.md`, `docs/PROGRESO.md`, `docs/GLOSARIO.md`
- **Decisions:** MVP = MC prices → cheapest / most expensive / in-season; parse real HTML
  (fixture) in Phase 1; normalize to price/kg; rank at product level; season = calendar + price signal.
- **Tests:** none yet (no implementation yet — docs only).
- **Next:** Stage 1 — Models (start with Product + tests).

---

## How to use this log

For each session, add:

```
## YYYY-MM-DD — Short title
- **What:** what you did in ~30 min.
- **Files:** which files changed.
- **Tests:** what tests passed / were added.
- **Next:** the next small step (or "stopped here").
```
