# Django sans DB

Tools for limiting access to the database in parts of your Django code.

## Installation

```
pip install django-sans-db
```

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

### Template backend

You can block access to the database when rendering Django templates with our custom template backend.

Note: Currently, only Django templates are supported.

You can block database access in all of your template renders
by setting `DjangoTemplatesSansDB` as your default template renderer.
To do so,
make sure the `"BACKEND"` key of your `TEMPLATES` setting has the value
`"sans_db.template_backends.django_sans_db.DjangoTemplatesSansDB"`.

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
