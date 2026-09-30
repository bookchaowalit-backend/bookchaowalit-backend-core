# Shared contracts

Canonical, versioned contract schemas shared by `bookchaowalit-backend`
repositories.

| Schema | Used by |
|---|---|
| [`book-platform.contract.v1.schema.json`](book-platform.contract.v1.schema.json) | `contract.json` in every Book Platform repository (`book-*-platform`, `book-api-gateway`) |

Each platform repository vendors an identical copy at
`schema/book-platform.contract.v1.schema.json` and validates its
`contract.json` offline with `scripts/check.py`. The schema digest is pinned in
[`book-platform.contract.v1.schema.json.sha256`](book-platform.contract.v1.schema.json.sha256)
(`sha256sum` format); platform repositories vendor the same pin file and fail
CI (`scripts/check_schema_pin.py`) when their copy drifts from it.

To change the schema: edit it here, regenerate the pin with
`(cd contracts && sha256sum book-platform.contract.v1.schema.json > book-platform.contract.v1.schema.json.sha256)`
(`scripts/check.py` fails until you do), then copy both files into every
platform repository in the same change set. With sibling checkouts,
`python3 scripts/check_platform_sync.py --workspace ..` reports any platform
whose schema or pin differs from this canonical copy.

The platform validators implement a JSON Schema subset (`type`, `const`,
`enum`, `pattern`, `minLength`, `minItems`, `uniqueItems`, `items`, `required`,
`properties`, `additionalProperties`, `$ref` to `#/$defs/...`).
`scripts/check.py` rejects a schema that uses any other keyword, so a rule
cannot be added here that the platform checks would silently ignore.

`examples/valid/` holds contracts that must pass and `examples/invalid/` holds
contracts that must fail; add a fixture with every schema change. Examples use
placeholder values only; never add credentials or customer data.

## Contract fields

- `schema_version`, `platform_id`, `repository`, `status`
  (`scaffolded`/`pilot`/`active`/`retired`), `api_version` (`vN`),
  `data_owner` (the repository or `none`).
- `capabilities` and `depends_on` (known platform ids only).
- `current_implementation`: `repository`, `source_path` (first entry of
  `source_paths`, or `none`), `source_paths`, `source_status`.
- `migration` (adapter, shadow parity, cutover, rollback) and
  `migration_gates`.
- `surface_doc` and `interfaces`: each interface has an `id`, `kind`
  (`http`, `event`, `cli`, `object-store`, `table`, `config`, `workflow`),
  `direction`, `name`, `status`, `source`, optional `contract` and `auth`. The
  platform check requires every interface id to appear in the surface document.
