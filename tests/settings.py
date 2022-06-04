from environs import Env


env = Env()


DATABASES = {
    "default": {},
    "mysql": env.dj_db_url("MYSQL_DATABASE_URL"),
    "postgres": env.dj_db_url("POSTGRES_DATABASE_URL"),
    "sqlite": env.dj_db_url("SQLITE_DATABASE_URL"),
}
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
