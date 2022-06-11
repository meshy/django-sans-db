from typing import Iterable, List, Union

from django import template

from ..context_managers import block_db


register = template.Library()


def _flatten(items: Iterable[Union[str, Iterable[str]]]) -> List[str]:
    flattened: List[str] = []
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, str):
            flattened.extend(item)
        else:
            flattened.append(item)

    return flattened


class SansDBNode(template.Node):
    def __init__(self, nodelist: template.NodeList, args: List[str]) -> None:
        self.nodelist = nodelist
        self.args = [template.Variable(arg) for arg in args]

    def render(self, context: template.Context) -> str:
        db_aliases = _flatten([var.resolve(context) for var in self.args])
        with block_db(databases=db_aliases or None):
            output = self.nodelist.render(context)
        return output


@register.tag
def sansdb(parser: template.base.Parser, token: template.base.Token) -> SansDBNode:
    """
    A tag for blocking DB access in a portion of your template.

    Raises DatabaseAccessBlocked when an attempt is made to access the database.

    Accepts database aliases as either strings, or variables.
    If passed as a variable, either strings or iterables of strings are accepted.
    If no aliases are passed, all databases will be blocked.

    Eg: To block all databases:

        {% load sansdb %}
        {% sansdb %}
            {# ... #}
        {% endsansdb %}

    Eg: To block databases named in the template:

        {% load sansdb %}
        {% sansdb "second_db" "third_db" %}
            {# ... #}
        {% endsansdb %}

    Eg: To block databases from a context variable:

        {% load sansdb %}
        {% sansdb databases %}
            {# ... #}
        {% endsansdb %}
    """
    _, *args = token.split_contents()
    nodelist = parser.parse(("endsansdb",))
    parser.delete_first_token()
    return SansDBNode(nodelist, args)
