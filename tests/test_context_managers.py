from typing import Tuple

import pytest

from sans_db.context_managers import block_db
from sans_db.exceptions import DatabaseAccessBlocked

from .models import ExampleModel


@pytest.mark.django_db(databases=["mysql", "postgres", "sqlite"])
class TestBlockDB:
    @pytest.mark.parametrize("database", ["mysql", "postgres", "sqlite"])
    def test_queryset_evaluation_blocked(self, database: str) -> None:
        queryset = ExampleModel.objects.using(database).all()
        with pytest.raises(DatabaseAccessBlocked):
            with block_db():
                list(queryset)

    @pytest.mark.parametrize("database", ["mysql", "postgres", "sqlite"])
    def test_evaluated_queryset_allowed(self, database: str) -> None:
        queryset = list(ExampleModel.objects.using(database).all())
        with block_db():
            for model in queryset:
                pass

    @pytest.mark.parametrize("blocked", ["mysql", "postgres", "sqlite"])
    def test_selective_blocking_blocked(self, blocked: str) -> None:
        with pytest.raises(DatabaseAccessBlocked):
            with block_db(databases=[blocked]):
                ExampleModel.objects.using(blocked).create()

    @pytest.mark.parametrize(
        "blocked, not_blocked",
        [
            ["mysql", ("postgres", "sqlite")],
            ["postgres", ("mysql", "sqlite")],
            ["sqlite", ("mysql", "postgres")],
        ],
    )
    def test_selective_blocking_allowed(
        self, blocked: str, not_blocked: Tuple[str, str]
    ) -> None:
        # No error raised, because queries aren't on blocked DB.
        with block_db(databases=[blocked]):
            for db in not_blocked:
                ExampleModel.objects.using(db).create()
