import pytest

from sans_db.context_managers import block_db
from sans_db.exceptions import DatabaseAccessBlocked

from .definitions import DATABASE_ALIASES
from .models import ExampleModel


@pytest.mark.django_db(databases=DATABASE_ALIASES)
class TestBlockDB:
    """Tests for block_db when used as a context manager."""

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_queryset_evaluation_blocked(self, database: str) -> None:
        queryset = ExampleModel.objects.using(database).all()
        with pytest.raises(DatabaseAccessBlocked):
            with block_db():
                list(queryset)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_evaluated_queryset_allowed(self, database: str) -> None:
        queryset = list(ExampleModel.objects.using(database).all())
        with block_db():
            list(queryset)

    @pytest.mark.parametrize("blocked", DATABASE_ALIASES)
    def test_selective_blocking_blocked(self, blocked: str) -> None:
        with pytest.raises(DatabaseAccessBlocked):
            with block_db(databases=[blocked]):
                ExampleModel.objects.using(blocked).create()

    @pytest.mark.parametrize("blocked", DATABASE_ALIASES)
    def test_selective_blocking_allowed(self, blocked: str) -> None:
        not_blocked = DATABASE_ALIASES - {blocked}
        # No error raised, because queries aren't on blocked DB.
        with block_db(databases=[blocked]):
            for db in not_blocked:
                ExampleModel.objects.using(db).create()
