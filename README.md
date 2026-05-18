# graphenda-shared

![CI](https://github.com/USER/graphenda-shared/workflows/CI/badge.svg)

Shared Python contract between the two Graphenda pillars:

- **`graphenda-build`** — offline graph engine (ingestion, transformation, materialization).
- **`graphenda-saas`** — online API serving the materialized graph.

This package is the **versioned contract** between them. Every change here implies a SemVer bump.

---

## What it contains

- `graphenda_shared.config` — common configuration (env loading, shared settings).
- `graphenda_shared.graph` — Neo4j interface: `connection`, `models`, `queries`.
- `graphenda_shared.models.core` — core domain models (`Entity`, `Relation`, …).
- `graphenda_shared.registry` — Pydantic models and YAML reader for the registry contract.

## What it is NOT

This package contains **no business logic**. It is the smallest set of types,
configuration and Neo4j primitives that **both** pillars need.

If a feature is used by only one pillar, it does **not** belong here — it belongs
inside that pillar.

---

## Installation

### Editable install from a sibling checkout (local development)

```bash
pip install -e ../graphenda-shared
```

### From a Git URL pinned to a tag (other projects, exact version)

```bash
pip install "graphenda-shared @ git+file:///home/guhaase/projetos/Graphenda/graphenda-shared@v0.1.0"
```

### In CI / production

Replace `file://` with the remote Git URL once the remote is defined
(see Decisao #2 of the master plan).

---

## Usage

```python
from graphenda_shared.graph.connection import get_driver
from graphenda_shared.registry.reader import load_registry
from graphenda_shared.models.core import Entity, Relation
```

Both `graphenda-build` and `graphenda-saas` pin an **exact** version of this
package in their `pyproject.toml`:

```toml
dependencies = [
    "graphenda-shared @ git+https://.../graphenda-shared@v0.1.0",
]
```

---

## Versioning (the contract)

This package follows **strict [SemVer](https://semver.org/spec/v2.0.0.html)**.
The `CHANGELOG.md` is mandatory: every release has an entry.

| Change type                                                 | Bump  | CHANGELOG section            |
| ----------------------------------------------------------- | ----- | ---------------------------- |
| Public API removed / renamed / signature changed (breaking) | major | `### Removed` / `### Changed`|
| New module / function / class (additive only)               | minor | `### Added`                  |
| Bug fix, no signature change                                | patch | `### Fixed`                  |

Every release requires an annotated Git tag:

```bash
git tag -a vX.Y.Z -m "graphenda-shared vX.Y.Z"
git push --tags
```

The **golden rule**: what lives in `graphenda-shared` is what **both** pillars
need. If only the Build uses it, move it to the Build.

---

## Local development

```bash
pip install -e ".[dev,test]"
make test
make lint
```

Available `make` targets: `install`, `lint`, `format`, `test`, `test-cov`, `clean`.

Pre-commit hooks are installed by `make install`; they run `ruff`, `black`,
`isort` and basic file hygiene checks.

---

## See also

- Master plan: [`../PLANO-DIVISAO-EM-PROJETOS.md`](../PLANO-DIVISAO-EM-PROJETOS.md), section 5.1
  (contract / versioning policy).
- `CHANGELOG.md` — every released version.
