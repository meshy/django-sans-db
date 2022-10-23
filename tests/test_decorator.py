import pytest

from sans_db.context_managers import block_db
from sans_db.exceptions import DatabaseAccessBlocked

from .definitions import DATABASE_ALIASES
from .models import ExampleModel


@pytest.mark.django_db(databases=DATABASE_ALIASES)
class TestBlockDBFunctionDecorator:
    """Tests for block_db when used as a function decorator."""

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_queryset_evaluation_blocked(self, database: str) -> None:
        queryset = ExampleModel.objects.using(database).all()

        @block_db()
        def func() -> None:
            list(queryset)

        with pytest.raises(DatabaseAccessBlocked):
            func()

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_evaluated_queryset_allowed(self, database: str) -> None:
        queryset = list(ExampleModel.objects.using(database).all())

        @block_db()
        def func() -> None:
            list(queryset)

        # No error raised, because query isn't on blocked DB.
        func()

    @pytest.mark.parametrize("blocked", DATABASE_ALIASES)
    def test_selective_blocking_blocked(self, blocked: str) -> None:
        @block_db(databases=[blocked])
        def func() -> None:
            ExampleModel.objects.using(blocked).create()

        with pytest.raises(DatabaseAccessBlocked):
            func()

    @pytest.mark.parametrize("blocked", DATABASE_ALIASES)
    def test_selective_blocking_allowed(self, blocked: str) -> None:
        @block_db(databases=[blocked])
        def func(db: str) -> None:
            ExampleModel.objects.using(db).create()

        # No error raised, because queries aren't on blocked DB.
        not_blocked = DATABASE_ALIASES - {blocked}
        for db in not_blocked:
            func(db)
