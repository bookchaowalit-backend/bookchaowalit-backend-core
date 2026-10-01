# Upgrade plan: bookchaowalit-backend-core

## Current state

Score: 5/10 (was 4/10 before pass 2). Still a starter with no runtime, but it
owns the canonical Book Platform contract schema with fixtures, a subset-aware
checker, a pinned digest that platform repositories enforce in CI, a workspace
sync check, tests and CI.

## Backlog

### P0

- Vendor the schema pin into `book-api-gateway` and `book-media-platform`
  (owned by another worker in pass 2); `scripts/check_platform_sync.py` warns
  that they have none. Then run it with `--require-pin`.
- Publish the platform `scripts/check.py` validator from here as the single
  source and have platform repositories vendor it the same way.

### P1

- Add shared event-envelope and error-body schemas once two platforms need the
  same shape (candidates: API Gateway error body, Data Bronze envelope).

### P2

- Decide the packaging for shared contracts (tagged releases or a small
  package) before any runtime consumer depends on them.

## Done in this pass (pass 2)

- `contracts/book-platform.contract.v1.schema.json.sha256` pins the schema
  digest; `scripts/check.py` fails when the pin is missing, malformed or stale.
- `scripts/check_platform_sync.py` compares every sibling platform checkout's
  vendored schema and pin with the canonical copy (local, read-only).
- The ten platform repositories in this pass vendor the pin and run
  `scripts/check_schema_pin.py` in CI (see their `docs/UPGRADE-PLAN.md`).
- `tests/test_platform_sync.py` (9 tests); `.gitignore` for Python caches;
  README and `contracts/README.md` document the change procedure.

## Done in pass 1

- `contracts/book-platform.contract.v1.schema.json` with valid and invalid
  example fixtures and `contracts/README.md`.
- `scripts/check.py` (baseline files, supported-keyword guard, fixture
  expectations) and `tests/test_check.py` (8 tests).
- CI runs the check and tests on every push and pull request; README and
  PRODUCT.md describe the actual state (removed the stale mobile-smoke note and
  duplicated README excerpt).
