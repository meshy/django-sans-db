import pytest
from django.template import engines
from django.template.exceptions import TemplateSyntaxError

from sans_db.exceptions import DatabaseAccessBlocked

from .definitions import DATABASE_ALIASES
from .models import ExampleModel


DJANGO_ENGINE = engines["django"]


@pytest.mark.django_db(databases=DATABASE_ALIASES)
class TestSansDBTemplateTag:
    def test_unclosed_tag(self) -> None:
        """The sansdb tag must be closed."""
        template_string = """
            {% load sansdb %}
            {% sansdb %}
        """

        with pytest.raises(TemplateSyntaxError):
            DJANGO_ENGINE.from_string(template_string)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_no_dbs(self, database: str) -> None:
        """When no DB is passed, all are blocked."""
        context = {"items": ExampleModel.objects.using(database).all()}
        template_string = """
            {% load sansdb %}
            {% sansdb %}
                {% for item in items %}{{ item.pk }}{% endfor %}
            {% endsansdb %}
        """

        template = DJANGO_ENGINE.from_string(template_string)

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_all_dbs(self, database: str) -> None:
        """When explicit DBs are passed, they are blocked."""
        context = {"items": ExampleModel.objects.using(database).all()}
        template_string = """
            {% load sansdb %}
            {% sansdb "mysql" "postgres" "sqlite" %}
                {% for item in items %}{{ item.pk }}{% endfor %}
            {% endsansdb %}
        """

        template = DJANGO_ENGINE.from_string(template_string)

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_variable_dbs(self, database: str) -> None:
        """When explicit DBs are passed as a list, they are blocked."""
        context = {
            "items": ExampleModel.objects.using(database).all(),
            "databases": [database],
        }
        template_string = """
            {% load sansdb %}
            {% sansdb databases %}
                {% for item in items %}{{ item.pk }}{% endfor %}
            {% endsansdb %}
        """

        template = DJANGO_ENGINE.from_string(template_string)

        with pytest.raises(DatabaseAccessBlocked):
            template.render(context)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_other_dbs(self, database: str) -> None:
        """When queries are not in the passed list, they are allowed."""
        context = {
            "items": ExampleModel.objects.using(database).all(),
            "databases": DATABASE_ALIASES - {database},
        }
        template_string = """
            {% load sansdb %}
            {% sansdb databases %}
                {% for item in items %}{{ item.pk }}{% endfor %}
            {% endsansdb %}
        """

        template = DJANGO_ENGINE.from_string(template_string)

        template.render(context)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_before_tag(self, database: str) -> None:
        """Queries before the tag are not blocked."""
        obj = ExampleModel.objects.using(database).create()
        context = {"items": ExampleModel.objects.using(database).all()}
        template_string = """
            {% load sansdb %}
            {% for item in items %}{{ item.pk }}{% endfor %}
            {% sansdb %}{% endsansdb %}
        """

        template = DJANGO_ENGINE.from_string(template_string)

        rendered = template.render(context)
        assert rendered.strip() == str(obj.pk)

    @pytest.mark.parametrize("database", DATABASE_ALIASES)
    def test_after_tag(self, database: str) -> None:
        """Queries after the tag are not blocked."""
        obj = ExampleModel.objects.using(database).create()
        context = {"items": ExampleModel.objects.using(database).all()}
        template_string = """
            {% load sansdb %}
            {% sansdb %}{% endsansdb %}
            {% for item in items %}{{ item.pk }}{% endfor %}
        """

        template = DJANGO_ENGINE.from_string(template_string)

        rendered = template.render(context)
        assert rendered.strip() == str(obj.pk)
