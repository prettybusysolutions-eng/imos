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

## Durable owner-scoped pilot

The API persists decisions in SQLite and isolates rows by authenticated owner.
Set `IMOS_DB_PATH` to durable storage and `IMOS_OWNER_KEY_HASHES` to a JSON object
mapping owner IDs to SHA256 hashes of distinct, high-entropy operator credentials.
Send the credential in `X-API-Key`. Use TLS outside localhost. Health is liveness;
`/ready` requires configured ownership and migrated storage. Duplicate decision
IDs within an owner return 409; the server acknowledges storage only after commit.

Schema version 1 is created transactionally at startup. Unknown schema versions
fail startup instead of silently rewriting data. Back up the database using SQLite
backup tooling and test restoring it before upgrades. Owner credentials are not a
browser identity service, and automated legacy-data migration is not implemented.

PR #16 includes useful graph and ingest exploration, but its unauthenticated path
based ingestion and deletion of current license/release files prevent wholesale
merging. This pilot deliberately exposes only decisions and owner-scoped summary;
graph inference, arbitrary filesystem ingestion and institutional-cognition claims
remain unvalidated. Tests exercise restart, duplicate handling and cross-owner denial.
