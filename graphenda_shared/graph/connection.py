"""Neo4j connection manager for Graphenda Engine."""

import logging
import os
from collections.abc import Generator
from contextlib import contextmanager
from types import TracebackType
from typing import Any

from neo4j import Driver, GraphDatabase, Session
from neo4j.exceptions import AuthError, ServiceUnavailable

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Manages Neo4j database connections."""

    def __init__(
        self,
        uri: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        self._uri: str = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self._user: str = user or os.environ.get("NEO4J_USER", "neo4j")
        self._password: str = password or os.environ.get("NEO4J_PASSWORD", "neo4j")
        self._driver: Driver | None = None

    @property
    def driver(self) -> Driver:
        """Lazy-initialize and return the Neo4j driver."""
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password),
            )
        return self._driver

    def connect(self) -> bool:
        """Explicitly connect and verify connectivity."""
        try:
            self.driver.verify_connectivity()
            logger.info("Neo4j connection OK: %s", self._uri)
            return True
        except ServiceUnavailable:
            logger.error("Neo4j unreachable at %s", self._uri)
            return False
        except AuthError:
            logger.error("Neo4j auth failed for user %s", self._user)
            return False

    @contextmanager
    def session(self, database: str = "neo4j") -> Generator[Session, None, None]:
        """Context manager for Neo4j sessions."""
        session = self.driver.session(database=database)
        try:
            yield session
        finally:
            session.close()

    def run(
        self, query: str, parameters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Execute a query and return results as list of dicts."""
        with self.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def close(self) -> None:
        """Close the driver connection."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

    def __enter__(self) -> "Neo4jConnection":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
