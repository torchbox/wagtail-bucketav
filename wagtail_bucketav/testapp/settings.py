import os

from wagtail import VERSION as WAGTAIL_VERSION

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "NAME": "wagtail_bucketav-test.sqlite",
        "ENGINE": "django.db.backends.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default-location",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

INSTALLED_APPS = [
    "wagtail_bucketav",
    "wagtail_bucketav.testapp",
    "modelcluster",
    "taggit",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "wagtail.admin",
    "wagtail" if WAGTAIL_VERSION >= (3, 0) else "wagtail.core",
    "wagtail.sites",
    "wagtail.search",
    "wagtail.users",
    "wagtail.images",
    "wagtail.documents",
    "wagtail.contrib.modeladmin",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "wagtail_bucketav.testapp.urls"
WAGTAIL_SITE_NAME = "WagtailBucketAV"
LOGIN_URL = "wagtailadmin_login"
LOGIN_REDIRECT_URL = "wagtailadmin_home"
SECRET_KEY = os.getenv("SECRET_KEY", "not-secret-at-all")

# Django i18n
TIME_ZONE = "Europe/London"
USE_TZ = True

# Used in Wagtail emails
BASE_URL = "https://localhost:8000"

# Don't redirect to HTTPS in tests
SECURE_SSL_REDIRECT = False

# Use default static files storage for tests
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")
STATIC_URL = "/static/"

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TODO: Unset when we have some model definitions in testapp.models :)
# WAGTAILIMAGES_IMAGE_MODEL = "testapp.CustomImage"
# WAGTAILDOCS_DOCUMENT_MODEL = "testapp.CustomDocument"
