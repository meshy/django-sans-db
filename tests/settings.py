from environs import Env


env = Env()


DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
SECRET_KEY = "only-for-tests"

INSTALLED_APPS = [
    "tests",
]

TEMPLATES = [
    {
        "BACKEND": "sans_db.template_backends.django_sans_db.DjangoTemplatesSansDB",
        "APP_DIRS": True,
    },
]
