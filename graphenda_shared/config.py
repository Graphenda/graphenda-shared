"""Shared configuration for Graphenda packages.

Loads settings from environment variables.
Build and SaaS extend this with their specific configs.
"""
import os
from dataclasses import dataclass


@dataclass
class Neo4jConfig:
    """Neo4j connection configuration."""
    uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user: str = os.getenv("NEO4J_USER", "neo4j")
    password: str = os.getenv("NEO4J_PASSWORD", "password")
    database: str = os.getenv("NEO4J_DATABASE", "neo4j")


@dataclass
class SharedConfig:
    """Base configuration shared between Build and SaaS."""
    neo4j: Neo4jConfig | None = None
    project_root: str = os.environ.get(
        "GRAPHENDA_ROOT",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )

    def __post_init__(self) -> None:
        if self.neo4j is None:
            self.neo4j = Neo4jConfig()
