# Changelog

All notable changes to `graphenda-shared` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] — 2026-05-18
### Fixed
- `RegistryReader.list_slugs()` was matching dotfiles (e.g. `.pre-commit-config.yaml`) because `pathlib.Path.glob` does not skip hidden files. Now filters out names starting with `.` in addition to `_`. Without this, `load_all()` raised `KeyError: 'slug'` when the registry repo had any tooling YAML at its root.

## [0.1.0] — 2026-05-18
### Added
- Initial extraction from monorepo (formerly `Graphenda/shared/`).
- `graphenda_shared.config` — common settings.
- `graphenda_shared.graph` — Neo4j connection, models and queries.
- `graphenda_shared.models.core` — domain entities and relations.
- `graphenda_shared.registry` — Pydantic models and YAML reader for the registry contract.
