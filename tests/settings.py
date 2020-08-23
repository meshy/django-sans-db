from environs import Env


env = Env()


DATABASES = {"default": env.dj_db_url("DATABASE_URL", default="postgres:///sansdb")}
SECRET_KEY = "only-for-tests"
