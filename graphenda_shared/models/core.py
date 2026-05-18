"""Modelos de dados compartilhados por toda a engine.

Estes modelos sao domain-agnostic — nenhuma referencia
a dominio especifico.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from pydantic import BaseModel


# --- Enums ---

class IntentType(str, Enum):
    VALIDATION = "validation"
    COMPARISON = "comparison"
    RECOMMENDATION = "recommendation"
    EXPLANATION = "explanation"
    CODE_EXAMPLE = "code_example"
    GENERAL = "general"


class RetrievalType(str, Enum):
    GRAPH = "graph"
    VECTOR = "vector"
    COMMUNITY = "community"
    HIERARCHICAL = "hierarchical"  # Fase 2


class ChunkType(str, Enum):
    PYTHON_CLASS = "python_class"
    PYTHON_FUNCTION = "python_function"
    PYTHON_MODULE = "python_module"
    MARKDOWN_SECTION = "markdown_section"
    NOTEBOOK_CELL_GROUP = "notebook_cell_group"
    PDF_SECTION = "pdf_section"
    CSV_METADATA = "csv_metadata"


# --- Data Models ---

@dataclass
class Chunk:
    chunk_id: str
    content: str
    chunk_type: ChunkType
    source_file: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def token_estimate(self) -> int:
        return len(self.content) // 4


class Entity(BaseModel):
    name: str
    type: str
    properties: dict[str, Any] = {}


class Relationship(BaseModel):
    source: str
    relation: str
    target: str
    properties: dict[str, Any] = {}


class Triple(BaseModel):
    subject: Entity
    predicate: str
    object: Entity
    confidence: float = 1.0
    source_chunk: str | None = None


@dataclass
class ParsedIntent:
    query: str
    entities: list[str]
    intent_type: IntentType
    retrieval_weights: dict[str, float]
    cypher_hints: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class RetrievalResult:
    content: str
    source: str
    score: float
    retrieval_type: RetrievalType
    metadata: dict[str, Any] = field(default_factory=dict)
