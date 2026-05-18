"""Smoke tests — only validate that public APIs exist and import cleanly.

These tests do NOT exercise behavior. They guard the public contract:
if a name disappears or is renamed, this suite fails and forces a
deliberate SemVer bump.
"""

import graphenda_shared


def test_package_has_version() -> None:
    assert hasattr(graphenda_shared, "__version__")
    assert graphenda_shared.__version__ == "0.1.1"


def test_imports_config() -> None:
    from graphenda_shared import config

    assert config is not None
    assert hasattr(config, "Neo4jConfig")
    assert hasattr(config, "SharedConfig")


def test_imports_graph_connection() -> None:
    from graphenda_shared.graph import connection

    assert connection is not None
    assert hasattr(connection, "Neo4jConnection")


def test_imports_graph_models() -> None:
    from graphenda_shared.graph import models

    assert models is not None
    assert hasattr(models, "Entity")
    assert hasattr(models, "Relationship")
    assert hasattr(models, "Triple")


def test_imports_graph_queries() -> None:
    from graphenda_shared.graph import queries

    assert queries is not None
    assert hasattr(queries, "CypherQueries")
    cq = queries.CypherQueries
    for method in (
        "find_by_name",
        "find_all",
        "find_any_by_name",
        "fuzzy_search",
        "get_entity_context",
        "get_neighbors",
        "find_by_relationship",
        "find_related",
        "compare_entities",
        "graph_stats",
        "relationship_stats",
        "find_by_level",
    ):
        assert hasattr(cq, method), f"CypherQueries.{method} missing"


def test_imports_models_core() -> None:
    from graphenda_shared.models import core

    assert core is not None
    for name in (
        "IntentType",
        "RetrievalType",
        "ChunkType",
        "Chunk",
        "Entity",
        "Relationship",
        "Triple",
        "ParsedIntent",
        "RetrievalResult",
    ):
        assert hasattr(core, name), f"models.core.{name} missing"


def test_imports_registry_models() -> None:
    from graphenda_shared.registry import models

    assert models is not None
    for name in (
        "GraphStatus",
        "GraphDomainConfig",
        "GraphMetrics",
        "GraphThresholds",
        "GraphRegistryEntry",
    ):
        assert hasattr(models, name), f"registry.models.{name} missing"


def test_imports_registry_reader() -> None:
    from graphenda_shared.registry import reader

    assert reader is not None
    assert hasattr(reader, "RegistryReader")


def test_registry_reader_skips_dotfiles_and_underscore(tmp_path) -> None:
    """list_slugs must skip both `_*.yaml` and `.*.yaml`."""
    from graphenda_shared.registry.reader import RegistryReader

    (tmp_path / "panelbox.yaml").write_text("slug: panelbox\n")
    (tmp_path / "_schema.yaml").write_text("slug: _schema\n")
    (tmp_path / ".pre-commit-config.yaml").write_text("repos: []\n")

    assert RegistryReader(tmp_path).list_slugs() == ["panelbox"]


def test_top_level_reexports() -> None:
    """Top-level package re-exports its main subpackages."""
    from graphenda_shared import config, graph, models, registry

    assert config is not None
    assert graph is not None
    assert models is not None
    assert registry is not None


def test_graph_package_reexports() -> None:
    """graphenda_shared.graph re-exports Neo4jConnection and core types."""
    from graphenda_shared import graph

    assert hasattr(graph, "Neo4jConnection")
    assert hasattr(graph, "Entity")
    assert hasattr(graph, "Relationship")
    assert hasattr(graph, "Triple")


def test_registry_package_reexports() -> None:
    """graphenda_shared.registry re-exports the public surface."""
    from graphenda_shared import registry

    for name in ("GraphRegistryEntry", "GraphStatus", "GraphMetrics", "RegistryReader"):
        assert hasattr(registry, name), f"registry.{name} missing"
