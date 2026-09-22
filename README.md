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

## Start here

Run the [five-minute quickstart](QUICKSTART.md) to start the API and verify its
health response. IMOS is currently an alpha service with in-process storage;
it is not yet a durable multi-tenant system.

Release status and gates: [RELEASING.md](RELEASING.md).

## Public API

- `GET /health` — liveness and service identity
- `/decisions` — decision-record operations
- `/context` — structured context operations

## License

MIT. See [LICENSE](LICENSE).
