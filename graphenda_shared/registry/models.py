"""Graph Registry shared models.

Used by both Build (to publish) and SaaS (to consume).
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class GraphStatus(str, Enum):
    """Lifecycle status of a graph in the registry."""
    BUILDING = "building"
    REVIEW = "review"
    ACTIVE = "active"
    DEPRECATED = "deprecated"


@dataclass
class GraphDomainConfig:
    """Visual and categorization config for a graph."""
    color: str = "#2563EB"
    icon: str = "database"
    category: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class GraphMetrics:
    """Current metrics of a graph."""
    nodes: int = 0
    edges: int = 0
    communities: int = 0
    avg_confidence: float = 0.0
    coverage: float = 0.0
    last_updated: str = ""


@dataclass
class GraphThresholds:
    """Quality thresholds for a graph."""
    min_confidence: float = 0.70
    min_nodes_for_active: int = 500
    curation_review_days: int = 30


@dataclass
class GraphRegistryEntry:
    """A single graph entry in the registry.

    This is the central data structure that describes a published graph.
    """
    slug: str
    name: str
    description: str
    version: str
    status: GraphStatus

    neo4j_database: str
    ontology: str
    hierarchy_levels: int = 4

    metrics: GraphMetrics = field(default_factory=GraphMetrics)
    retrievers: list[str] = field(default_factory=lambda: ["graph", "vector", "community", "hierarchical", "curated"])
    domain: GraphDomainConfig = field(default_factory=GraphDomainConfig)
    thresholds: GraphThresholds = field(default_factory=GraphThresholds)

    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    def is_available(self) -> bool:
        """Whether this graph is available for SaaS clients."""
        return self.status == GraphStatus.ACTIVE

    def meets_publish_criteria(self) -> tuple[bool, list[str]]:
        """Check if graph meets criteria to be published as active.

        Returns:
            Tuple of (meets_criteria, list_of_issues).
        """
        issues = []
        if self.metrics.nodes < self.thresholds.min_nodes_for_active:
            issues.append(
                f"Nodes ({self.metrics.nodes}) below minimum ({self.thresholds.min_nodes_for_active})"
            )
        if self.metrics.avg_confidence < self.thresholds.min_confidence:
            issues.append(
                f"Confidence ({self.metrics.avg_confidence:.0%}) below minimum ({self.thresholds.min_confidence:.0%})"
            )
        return len(issues) == 0, issues
