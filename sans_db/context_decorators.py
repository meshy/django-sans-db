from contextlib import contextmanager
from typing import Iterator, List

from django.db import connection

from .exceptions import DatabaseAccessBlocked


@contextmanager
def block_db() -> Iterator[None]:
    def blocker(*args: List) -> None:
        raise DatabaseAccessBlocked

    with connection.execute_wrapper(blocker):
        yield
