from contextlib import ExitStack, contextmanager
from typing import Iterator, List, Optional

from django.db import connections

from .exceptions import DatabaseAccessBlocked


def _blocker(*args: object) -> None:
    raise DatabaseAccessBlocked


@contextmanager
def block_db(*, databases: Optional[List[str]] = None) -> Iterator[None]:
    if databases is None:
        databases = list(connections)

    to_block = [connections[db_alias] for db_alias in databases]
    managers = [connection.execute_wrapper(_blocker) for connection in to_block]

    with ExitStack() as stack:
        for manager in managers:
            stack.enter_context(manager)
        yield
