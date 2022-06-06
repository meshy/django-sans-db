from django.conf import settings


DATABASE_ALIASES = {alias for alias in settings.DATABASES.keys() if alias != "default"}
