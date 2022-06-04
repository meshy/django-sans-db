import pytest
from django.template import engines
from django.template.backends.django import Template

from sans_db.exceptions import DatabaseAccessBlocked
from sans_db.template_backends.django_sans_db import TemplateSansDB

from ..models import ExampleModel


DJANGO_ENGINE = engines["django_sans_db"]
TEMPLATE_STRING = "{% for item in items %}{{ item.pk }}{% endfor %}"


@pytest.mark.django_db
class TestDjangoTemplatesSansDB:
    def test_from_string_type(self) -> None:
        template = DJANGO_ENGINE.from_string(TEMPLATE_STRING)
        assert isinstance(template, Template)
        assert isinstance(template, TemplateSansDB)

    def test_query_in_template_string(self) -> None:
        database = "default"
        context = {"items": ExampleModel.objects.using(database).all()}
        template = DJANGO_ENGINE.from_string(TEMPLATE_STRING)

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    def test_no_query_in_template_string(self) -> None:
        database = "default"
        obj = ExampleModel.objects.using(database).create()
        context = {"items": list(ExampleModel.objects.using(database).all())}
        template = DJANGO_ENGINE.from_string(TEMPLATE_STRING)

        rendered = template.render(context)

        assert rendered == str(obj.pk)

    def test_get_template_type(self) -> None:
        template = DJANGO_ENGINE.get_template("django_template.html")
        assert isinstance(template, Template)
        assert isinstance(template, TemplateSansDB)

    def test_query_in_template_file(self) -> None:
        database = "default"
        obj = ExampleModel.objects.using(database).create()
        context = {"items": ExampleModel.objects.using(database).all()}
        template = DJANGO_ENGINE.get_template("django_template.html")

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    def test_no_query_in_template_file(self) -> None:
        database = "default"
        obj = ExampleModel.objects.using(database).create()
        items = list(ExampleModel.objects.using(database).all())
        context = {"items": items}

        template = DJANGO_ENGINE.get_template("django_template.html")

        rendered = template.render(context)
        assert str(obj.pk) in rendered
