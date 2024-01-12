import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "NAME": "django_bucketav-test.sqlite",
        "ENGINE": "django.db.backends.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default-location",
    },
}

INSTALLED_APPS = [
    "django_bucketav",
    "django_bucketav.testapp",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "django_bucketav.testapp.urls"
SECRET_KEY = os.getenv("SECRET_KEY", "not-secret-at-all")

TIME_ZONE = "Europe/London"
USE_TZ = True

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"

# And finally, our own package's settings:
BUCKETAV_MODELS = {
    "testapp.Document": ["file"],
}
