# Django sans DB

Tools for limiting access to the database in parts of your Django code.

## Installation

```
pip install django-sans-db
```

If you wish to use the `{% sansdb %}` template tag,
you will need to add `"sans_db"` to your `INSTALLED_APPS`.

## Usage

### Context manager

You can block access to your database for a section of your code using `block_db`:

```python
from sans_db.context_managers import block_db

User.objects.create(...)  # Works outside of block_db()
with block_db():
    User.objects.get()  # Raises DatabaseAccessBlocked
```

If you have multiple entries in your Django `DATABASES` setting,
then `block_db` will default to blocking all of them.

If you wish to block access to a subset of your databases,
pass a list of their aliases (the keys in the `DATABASES` dictionary).

```python
from sans_db.context_managers import block_db

with block_db(databases=["replica"]):
    User.objects.using("primary").create(...)  # This DB isn't blocked.
    User.objects.using("replica").get()  # Raises DatabaseAccessBlocked
```


### Decorator

You can decorate functions and methods with `block_db` to block database access in them. Eg:

```python
from sans_db.context_managers import block_db

class MyClass:
    def allowed(self):
        User.objects.create(...)  # Works outside of block_db()

    @block_db()
    def not_allowed(self):
        User.objects.create(...)  # Raises DatabaseAccessBlocked
```


### Template backend

You can block access to the database when rendering Django templates with our custom template backend.

Note: Currently, only Django templates are supported.

You can block database access in all of your templates
by setting your templates backend to `"sans_db.template_backends.django_sans_db.DjangoTemplatesSansDB"`

For example:

```python
# settings.py

TEMPLATES = [
    {
        "BACKEND": "sans_db.template_backends.django_sans_db.DjangoTemplatesSansDB",
        "APP_DIRS": True,
        "OPTIONS": {...},
    },
]
```

Attempts to query the database will now cause a `sans_db.exceptions.DatabaseAccessBlocked` to be raised.

Please refer to Django's docs on [support for template engines](https://docs.djangoproject.com/en/4.0/topics/templates/#support-for-template-engines)
for details on how to set this up as a secondary template renderer.


### Template tag

You can block DB access in a portion of your template
by wrapping it with the `{% sansdb %}` template tag.

The template tag accepts database aliases as either strings, or variables.
If passed as a variable, either strings or iterables of strings are accepted.
If no aliases are passed, all databases will be blocked.

Note: `DatabaseAccessBlocked` is raised when an attempt is made to access the DB.

To block all databases:

```django
{% load sansdb %}
{% sansdb %}
    {# ... #}
{% endsansdb %}
```

To block a list of databases named in the template:

```django
{% load sansdb %}
{% sansdb "second_db" "third_db" %}
    {# ... #}
{% endsansdb %}
```

To block a list of databases from a context variable:

```django
{% load sansdb %}
{% sansdb databases %}
    {# ... #}
{% endsansdb %}
```
