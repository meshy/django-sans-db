from typing import Dict, List, Union

from django.http import HttpRequest
from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates, Template, reraise

from sans_db.context_decorators import block_db


class TemplateSansDB(Template):
    def render(self, context: Dict = None, request: HttpRequest = None) -> str:
        with block_db():
            return super().render(context, request)


class DjangoTemplatesSansDB(DjangoTemplates):
    def from_string(self, template_code: str) -> TemplateSansDB:
        return TemplateSansDB(self.engine.from_string(template_code), self)

    def get_template(self, template_name: str) -> TemplateSansDB:  # type: ignore[return]
        try:
            return TemplateSansDB(self.engine.get_template(template_name), self)
        except TemplateDoesNotExist as exc:
            # This line always throws an exception, by mypy doesn't know that.
            reraise(exc, self)
