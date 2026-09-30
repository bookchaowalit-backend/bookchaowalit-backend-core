# bookchaowalit-backend-core — Product brief

**Slug:** `bookchaowalit-backend/bookchaowalit-backend-core`  
**Generated:** 2026-08-11 (bulk Book Dev closeout)  
**Status:** starter / portfolio boundary

## Purpose

Portfolio repository under Book Dev. This brief records ownership and the
current honest status so the nested tree is not an empty shell in the task
system.

## Runnable path

`python3 scripts/check.py` and `python3 -m unittest discover -s tests` (Python
3.11+, no dependencies). See `README.md`.

## Shared contracts

- `contracts/book-platform.contract.v1.schema.json`: canonical schema for the
  Book Platform repository contracts, vendored by each platform repository.

## Limits

- No runtime, service or worker exists yet; nothing here is production-ready.
- Schema changes must be copied to every platform repository that vendors them.
