from contextlib import ExitStack, contextmanager
from typing import Iterator

from django.db import connections

from .exceptions import DatabaseAccessBlocked


@contextmanager
def block_db() -> Iterator[None]:
    def blocker(*args: object) -> None:
        raise DatabaseAccessBlocked

    databases = list(connections)
    to_block = [connections[db_alias] for db_alias in databases]
    managers = [connection.execute_wrapper(blocker) for connection in to_block]

    with ExitStack() as stack:
        for manager in managers:
            stack.enter_context(manager)
        yield
