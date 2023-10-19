from .base import *
import environ

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8t-0p(a-pb84lht&b(*6!w28x00#e%g#ijm%(n6^szvh9)$vwn"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
