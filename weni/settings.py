"""
Django settings for weni project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

import environ
import sentry_sdk
from django.utils.log import DEFAULT_LOGGING
from django.utils.translation import ugettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

environ.Env.read_env(env_file=(environ.Path(__file__) - 2)(".env"))

env = environ.Env(
    # set casting, default value
    ENVIRONMENT=(str, "production"),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(lambda v: [s.strip() for s in v.split(",")], "*"),
    LANGUAGE_CODE=(str, "en-us"),
    TIME_ZONE=(str, "UTC"),
    STATIC_URL=(str, "/static/"),
    CELERY_BROKER_URL=(str, "redis://localhost:6379/0"),
    AWS_ACCESS_KEY_ID=(str, None),
    AWS_SECRET_ACCESS_KEY=(str, None),
    AWS_STORAGE_BUCKET_NAME=(str, None),
    AWS_S3_REGION_NAME=(str, None),
    EMAIL_HOST=(lambda v: v or None, None),
    DEFAULT_FROM_EMAIL=(str, "webmaster@localhost"),
    SERVER_EMAIL=(str, "root@localhost"),
    EMAIL_PORT=(int, 25),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_SSL=(bool, False),
    EMAIL_USE_TLS=(bool, False),
    SEND_EMAILS=(bool, True),
    CSRF_COOKIE_DOMAIN=(lambda v: v or None, None),
    CSRF_COOKIE_SECURE=(bool, False),
    BASE_URL=(str, "https://api.weni.ai"),
    WEBAPP_BASE_URL=(str, "https://dash.weni.ai"),
    INTELIGENCE_URL=(str, "https://bothub.it/"),
    FLOWS_URL=(str, "https://new.push.al/"),
    USE_SENTRY=(bool, False),
    SENTRY_URL=(str, None),
    APM_DISABLE_SEND=(bool, False),
    APM_SERVICE_DEBUG=(bool, False),
    APM_SERVICE_NAME=(str, ""),
    APM_SECRET_TOKEN=(str, ""),
    APM_SERVER_URL=(str, ""),
    FLOW_GRPC_ENDPOINT=(str, "localhost:8002"),
    INTELIGENCE_GRPC_ENDPOINT=(str, "localhost:8003"),
    SYNC_ORGANIZATION_INTELIGENCE=(bool, False),
    INTELIGENCE_CERTIFICATE_GRPC_CRT=(str, None),
    FLOW_CERTIFICATE_GRPC_CRT=(str, None),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

BASE_URL = env.str("BASE_URL")

WEBAPP_BASE_URL = env.str("WEBAPP_BASE_URL")

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg2",
    "django_filters",
    "mozilla_django_oidc",
    "elasticapm.contrib.django",
    "weni.authentication.apps.AuthenticationConfig",
    "weni.common.apps.CommonConfig",
    "django_celery_results",
    "django_celery_beat",
    "storages",
    "corsheaders",
    "django_grpc_framework",
]

MIDDLEWARE = [
    "elasticapm.contrib.django.middleware.TracingMiddleware",
    "elasticapm.contrib.django.middleware.Catch404Middleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "weni.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "elasticapm.contrib.django.context_processors.rum_tracing",
            ]
        },
    }
]

WSGI_APPLICATION = "weni.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": env.db(var="DEFAULT_DATABASE", default="sqlite:///db.sqlite3")}


# Auth

AUTH_USER_MODEL = "authentication.User"


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = env.str("LANGUAGE_CODE")

# -----------------------------------------------------------------------------------
# Available languages for translation
# -----------------------------------------------------------------------------------
LANGUAGES = (
    ("en-us", _("English")),
    ("pt-br", _("Portuguese")),
)

DEFAULT_LANGUAGE = "en-us"

TIME_ZONE = env.str("TIME_ZONE")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = env.str("STATIC_URL")

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Logging

LOGGING = DEFAULT_LOGGING
LOGGING["handlers"]["elasticapm"] = {
    "level": "WARNING",
    "class": "elasticapm.contrib.django.handlers.LoggingHandler",
}
LOGGING["formatters"]["verbose"] = {
    "format": "%(levelname)s  %(asctime)s  %(module)s "
    "%(process)d  %(thread)d  %(message)s"
}
LOGGING["handlers"]["console"] = {
    "level": "DEBUG",
    "class": "logging.StreamHandler",
    "formatter": "verbose",
}
LOGGING["loggers"]["django.db.backends"] = {
    "level": "ERROR",
    "handlers": ["console"],
    "propagate": False,
}
LOGGING["loggers"]["sentry.errors"] = {
    "level": "DEBUG",
    "handlers": ["console"],
    "propagate": False,
}
LOGGING["loggers"]["elasticapm.errors"] = {
    "level": "ERROR",
    "handlers": ["console"],
    "propagate": False,
}
LOGGING["loggers"]["weni.authentication.signals"] = {
    "level": "ERROR",
    "handlers": ["console"],
    "propagate": False,
}

# rest framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

if TESTING:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
        "rest_framework.authentication.TokenAuthentication"
    )

# CSRF

CSRF_COOKIE_DOMAIN = env.str("CSRF_COOKIE_DOMAIN")

CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE")

# Sentry Environment

USE_SENTRY = env.bool("USE_SENTRY")


# Sentry

if USE_SENTRY:
    sentry_sdk.init(
        dsn=env.str("SENTRY_URL"),
        integrations=[DjangoIntegration()],
        environment=env.str("ENVIRONMENT"),
    )

# Elastic Observability APM
ELASTIC_APM = {
    "DISABLE_SEND": env.bool("APM_DISABLE_SEND"),
    "DEBUG": env.bool("APM_SERVICE_DEBUG"),
    "SERVICE_NAME": env.str("APM_SERVICE_NAME"),
    "SECRET_TOKEN": env.str("APM_SECRET_TOKEN"),
    "SERVER_URL": env.str("APM_SERVER_URL"),
    "ENVIRONMENT": env.str("ENVIRONMENT"),
    "DJANGO_TRANSACTION_NAME_FROM_ROUTE": True,
    "PROCESSORS": (
        "elasticapm.processors.sanitize_stacktrace_locals",
        "elasticapm.processors.sanitize_http_request_cookies",
        "elasticapm.processors.sanitize_http_headers",
        "elasticapm.processors.sanitize_http_wsgi_env",
        "elasticapm.processors.sanitize_http_request_querystring",
        "elasticapm.processors.sanitize_http_request_body",
    ),
}

# mozilla-django-oidc
OIDC_RP_SERVER_URL = env.str("OIDC_RP_SERVER_URL")
OIDC_RP_REALM_NAME = env.str("OIDC_RP_REALM_NAME")
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")
OIDC_OP_AUTHORIZATION_ENDPOINT = env.str("OIDC_OP_AUTHORIZATION_ENDPOINT")
OIDC_OP_TOKEN_ENDPOINT = env.str("OIDC_OP_TOKEN_ENDPOINT")
OIDC_OP_USER_ENDPOINT = env.str("OIDC_OP_USER_ENDPOINT")
OIDC_OP_JWKS_ENDPOINT = env.str("OIDC_OP_JWKS_ENDPOINT")
OIDC_RP_SIGN_ALGO = env.str("OIDC_RP_SIGN_ALGO", default="RS256")
OIDC_DRF_AUTH_BACKEND = env.str(
    "OIDC_DRF_AUTH_BACKEND",
    default="weni.oidc_authentication.WeniOIDCAuthenticationBackend",
)
OIDC_RP_SCOPES = env.str("OIDC_RP_SCOPES", default='openid email')

# Swagger

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "DOC_EXPANSION": "list",
    "APIS_SORTER": "alpha",
    "SECURITY_DEFINITIONS": {
        "OIDC": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

# Celery

CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

# AWS

AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME")

# cors headers

CORS_ORIGIN_ALLOW_ALL = True

# mail

envvar_EMAIL_HOST = env.str("EMAIL_HOST")

EMAIL_SUBJECT_PREFIX = "[weni] "
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env.str("SERVER_EMAIL")

if envvar_EMAIL_HOST:
    EMAIL_HOST = envvar_EMAIL_HOST
    EMAIL_PORT = env.int("EMAIL_PORT")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SEND_EMAILS = env.bool("SEND_EMAILS")

# Products URL

INTELIGENCE_URL = env.str("INTELIGENCE_URL")
FLOWS_URL = env.str("FLOWS_URL")

FLOW_GRPC_ENDPOINT = env.str("FLOW_GRPC_ENDPOINT")
INTELIGENCE_GRPC_ENDPOINT = env.str("INTELIGENCE_GRPC_ENDPOINT")

SYNC_ORGANIZATION_INTELIGENCE = env.bool("SYNC_ORGANIZATION_INTELIGENCE")

INTELIGENCE_CERTIFICATE_GRPC_CRT = env.str("INTELIGENCE_CERTIFICATE_GRPC_CRT")
FLOW_CERTIFICATE_GRPC_CRT = env.bool("FLOW_CERTIFICATE_GRPC_CRT")
