import pytest
from django.template import engines
from django.template.backends.django import Template

from sans_db.exceptions import DatabaseAccessBlocked
from sans_db.template_backends.django_sans_db import TemplateSansDB

from ..definitions import DATABASE_ALIASES
from ..models import ExampleModel


DJANGO_ENGINE = engines["django_sans_db"]
TEMPLATE_STRING = "{% for item in items %}{{ item.pk }}{% endfor %}"


@pytest.mark.django_db(databases=DATABASE_ALIASES)
class TestDjangoTemplatesSansDB:
    def test_from_string_type(self) -> None:
        template = DJANGO_ENGINE.from_string(TEMPLATE_STRING)
        assert isinstance(template, Template)
        assert isinstance(template, TemplateSansDB)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_query_in_template_string(self, database: str) -> None:
        context = {"items": ExampleModel.objects.using(database).all()}
        template = DJANGO_ENGINE.from_string(TEMPLATE_STRING)

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_no_query_in_template_string(self, database: str) -> None:
        obj = ExampleModel.objects.using(database).create()
        context = {"items": list(ExampleModel.objects.using(database).all())}
        template = DJANGO_ENGINE.from_string(TEMPLATE_STRING)

        rendered = template.render(context)

        assert rendered == str(obj.pk)

    def test_get_template_type(self) -> None:
        template = DJANGO_ENGINE.get_template("django_template.html")
        assert isinstance(template, Template)
        assert isinstance(template, TemplateSansDB)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_query_in_template_file(self, database: str) -> None:
        obj = ExampleModel.objects.using(database).create()
        context = {"items": ExampleModel.objects.using(database).all()}
        template = DJANGO_ENGINE.get_template("django_template.html")

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_no_query_in_template_file(self, database: str) -> None:
        obj = ExampleModel.objects.using(database).create()
        items = list(ExampleModel.objects.using(database).all())
        context = {"items": items}

        template = DJANGO_ENGINE.get_template("django_template.html")

        rendered = template.render(context)
        assert str(obj.pk) in rendered
