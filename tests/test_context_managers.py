import pytest

from sans_db.context_managers import block_db
from sans_db.exceptions import DatabaseAccessBlocked

from .models import ExampleModel


@pytest.mark.django_db
class TestBlockDB:
    def test_queryset_evaluation_blocked(self) -> None:
        database = "default"
        queryset = ExampleModel.objects.using(database).all()
        with pytest.raises(DatabaseAccessBlocked):
            with block_db():
                list(queryset)

    def test_evaluated_queryset_allowed(self) -> None:
        database = "default"
        ExampleModel.objects.using(database).create()
        queryset = list(ExampleModel.objects.using(database).all())
        with block_db():
            for model in queryset:
                pass
