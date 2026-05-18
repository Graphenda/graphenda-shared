"""Parametrized Cypher query templates for Graphenda Engine.

All queries accept entity_type as a parameter so they are
domain-agnostic and driven by the ontology.
"""


class CypherQueries:
    """Generates Cypher queries parametrized by entity type."""

    # ------------------------------------------------------------------
    # Entity lookup
    # ------------------------------------------------------------------

    @staticmethod
    def find_by_name(entity_type: str) -> str:
        """MATCH a single entity by name and type."""
        label = entity_type.replace(" ", "_")
        return f"MATCH (n:{label} {{name: $name}}) RETURN n"

    @staticmethod
    def find_all(entity_type: str, limit: int = 100) -> str:
        """Return all entities of a given type."""
        label = entity_type.replace(" ", "_")
        return f"MATCH (n:{label}) RETURN n LIMIT {limit}"

    @staticmethod
    def find_any_by_name() -> str:
        """Find an entity by name regardless of type."""
        return "MATCH (n {name: $name}) RETURN n, labels(n)[0] AS type"

    @staticmethod
    def fuzzy_search() -> str:
        """Full-text fuzzy search across entity types."""
        return (
            "CALL db.index.fulltext.queryNodes($index_name, $search_term) "
            "YIELD node, score "
            "WHERE score > $min_score "
            "RETURN node, labels(node)[0] AS type, score "
            "ORDER BY score DESC LIMIT $limit"
        )

    # ------------------------------------------------------------------
    # Neighborhood / context
    # ------------------------------------------------------------------

    @staticmethod
    def get_entity_context(entity_type: str) -> str:
        """Get an entity with all its direct relationships."""
        label = entity_type.replace(" ", "_")
        return (
            f"MATCH (e:{label} {{name: $name}}) "
            "OPTIONAL MATCH (e)-[r]->(out) "
            "OPTIONAL MATCH (inp)-[r2]->(e) "
            "RETURN e, "
            "collect(DISTINCT {rel: type(r), target: out.name, target_type: labels(out)[0]}) AS outgoing, "
            "collect(DISTINCT {rel: type(r2), source: inp.name, source_type: labels(inp)[0]}) AS incoming"
        )

    @staticmethod
    def get_neighbors(entity_type: str, depth: int = 1) -> str:
        """Get neighbors up to N hops from an entity."""
        label = entity_type.replace(" ", "_")
        return (
            f"MATCH (e:{label} {{name: $name}})-[r*1..{depth}]-(neighbor) "
            "RETURN DISTINCT neighbor, labels(neighbor)[0] AS type"
        )

    # ------------------------------------------------------------------
    # Relationship-specific
    # ------------------------------------------------------------------

    @staticmethod
    def find_by_relationship(
        source_type: str, rel_type: str, target_type: str
    ) -> str:
        """Find entities connected by a specific relationship."""
        src = source_type.replace(" ", "_")
        tgt = target_type.replace(" ", "_")
        return (
            f"MATCH (s:{src})-[r:{rel_type}]->(t:{tgt}) "
            "RETURN s, r, t"
        )

    @staticmethod
    def find_related(entity_type: str, rel_type: str) -> str:
        """Find all targets related to an entity via a relationship type."""
        label = entity_type.replace(" ", "_")
        return (
            f"MATCH (e:{label} {{name: $name}})-[:{rel_type}]->(t) "
            "RETURN t, labels(t)[0] AS type"
        )

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    @staticmethod
    def compare_entities(entity_type: str) -> str:
        """Compare two entities of the same type."""
        label = entity_type.replace(" ", "_")
        return (
            f"MATCH (e1:{label} {{name: $name1}}) "
            f"MATCH (e2:{label} {{name: $name2}}) "
            "OPTIONAL MATCH (e1)-[r]-(e2) "
            "RETURN e1, e2, collect({rel: type(r), props: properties(r)}) AS connections"
        )

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    @staticmethod
    def graph_stats() -> str:
        """Count nodes per label."""
        return (
            "MATCH (n) "
            "WITH labels(n)[0] AS label, count(n) AS count "
            "RETURN label, count ORDER BY count DESC"
        )

    @staticmethod
    def relationship_stats() -> str:
        """Count relationships per type."""
        return (
            "MATCH ()-[r]->() "
            "WITH type(r) AS type, count(r) AS count "
            "RETURN type, count ORDER BY count DESC"
        )

    # ------------------------------------------------------------------
    # Level-based queries
    # ------------------------------------------------------------------

    @staticmethod
    def find_by_level(entity_types_at_level: list[str]) -> str:
        """Find all entities at a given ontology level."""
        labels = "|".join(t.replace(" ", "_") for t in entity_types_at_level)
        return f"MATCH (n:{labels}) RETURN n, labels(n)[0] AS type"
