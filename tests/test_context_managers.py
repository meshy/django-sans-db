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
