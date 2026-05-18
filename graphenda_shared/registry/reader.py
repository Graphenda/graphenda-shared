"""Graph Registry reader — loads registry entries from YAML files.

Used by both Build and SaaS to read the registry.
"""
import yaml
from pathlib import Path
from graphenda_shared.registry.models import (
    GraphRegistryEntry,
    GraphStatus,
    GraphMetrics,
    GraphDomainConfig,
    GraphThresholds,
)


class RegistryReader:
    """Reads graph registry entries from YAML files."""

    def __init__(self, registry_dir: str | Path):
        self.registry_dir = Path(registry_dir)

    def list_slugs(self) -> list[str]:
        """List all graph slugs in the registry."""
        return [
            f.stem
            for f in self.registry_dir.glob("*.yaml")
            if not f.name.startswith(("_", "."))
        ]

    def load(self, slug: str) -> GraphRegistryEntry:
        """Load a single registry entry by slug."""
        path = self.registry_dir / f"{slug}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Registry entry not found: {slug}")

        with open(path) as f:
            data = yaml.safe_load(f)

        return GraphRegistryEntry(
            slug=data["slug"],
            name=data["name"],
            description=data.get("description", ""),
            version=data["version"],
            status=GraphStatus(data["status"]),
            neo4j_database=data["neo4j_database"],
            ontology=data["ontology"],
            hierarchy_levels=data.get("hierarchy_levels", 4),
            metrics=GraphMetrics(**data.get("metrics", {})),
            retrievers=data.get("retrievers", []),
            domain=GraphDomainConfig(**data.get("domain", {})),
            thresholds=GraphThresholds(**data.get("thresholds", {})),
        )

    def load_all(self) -> list[GraphRegistryEntry]:
        """Load all registry entries."""
        return [self.load(slug) for slug in self.list_slugs()]

    def load_active(self) -> list[GraphRegistryEntry]:
        """Load only active registry entries (available for SaaS)."""
        return [e for e in self.load_all() if e.is_available()]
