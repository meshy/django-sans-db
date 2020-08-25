from environs import Env


env = Env()


DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
SECRET_KEY = "only-for-tests"
