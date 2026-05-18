"""Graph-specific models for Graphenda Engine.

Re-exports core models used by the graph layer and adds
graph-specific types when needed.
"""

from graphenda_shared.models.core import Entity, Relationship, Triple

__all__ = ["Entity", "Relationship", "Triple"]
