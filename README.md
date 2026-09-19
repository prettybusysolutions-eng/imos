# IMOS

Internal management operating standard and deployment frameworks.

IMOS is the operator kit layer for institutional memory, operational discipline, attribution, and managed continuity across real work.

## Role in the system
When the standard needs to persist, it needs a management surface.
This repository exists to keep operational knowledge structured, reusable, and enforceable.

## Standard
Capture the decision.
Preserve the context.
Keep the standard intact.

## What it is

Persistent organizational cognition: decisions, verification, attribution, blockers, and institutional memory as an executable system.

## Recovered implementation

The v0.3 backup implementation now provides database-backed decisions, entities,
edges, blockers, and local ingestion. Set `IMOS_DATABASE_URL` to choose the
database (default: `sqlite:///./imos.db`). Start with
`uvicorn imos.app:app --host 127.0.0.1 --port 8000`.

Install `requirements.txt`, then `pytest httpx`, and run `python -m pytest -q`.
Tests use an isolated database and verify decisions across a process restart.
This remains local operator tooling: ingestion reads operator-selected paths;
authentication and public multi-tenant hosting are not provided.
