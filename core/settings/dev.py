from .base import *
from decouple import config
SECRET_KEY = "dev-secret-key"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "soundora",
        "USER": "alidb",
        "PASSWORD": "ali72387238",
        "HOST": "postgres_db",
        "PORT": "5432",
    }
}
