from contextlib import contextmanager
from typing import Iterator

from django.db import connection

from .exceptions import DatabaseAccessBlocked


@contextmanager
def block_db() -> Iterator[None]:
    def blocker(*args: object) -> None:
        raise DatabaseAccessBlocked

    with connection.execute_wrapper(blocker):
        yield
