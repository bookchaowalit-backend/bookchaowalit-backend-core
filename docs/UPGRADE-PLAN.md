# Upgrade plan: bookchaowalit-backend-core

## Current state

Score: 4/10 (was 2/10). Still a starter with no runtime, but it now owns the
canonical Book Platform contract schema with fixtures, a subset-aware checker,
tests and CI.

## Backlog

### P0

- Add a sync check (script or reusable workflow) that fails when a platform
  repository's vendored `schema/book-platform.contract.v1.schema.json` differs
  from `contracts/`; today the copies are kept identical by hand.
- Publish the platform `scripts/check.py` validator from here as the single
  source and have platform repositories vendor it the same way.

### P1

- Add shared event-envelope and error-body schemas once two platforms need the
  same shape (candidates: API Gateway error body, Data Bronze envelope).

### P2

- Decide the packaging for shared contracts (tagged releases or a small
  package) before any runtime consumer depends on them.

## Done in this pass

- `contracts/book-platform.contract.v1.schema.json` with valid and invalid
  example fixtures and `contracts/README.md`.
- `scripts/check.py` (baseline files, supported-keyword guard, fixture
  expectations) and `tests/test_check.py` (8 tests).
- CI runs the check and tests on every push and pull request; README and
  PRODUCT.md describe the actual state (removed the stale mobile-smoke note and
  duplicated README excerpt).
