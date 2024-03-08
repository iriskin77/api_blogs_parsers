"""
Django settings for parser project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from .logging_formatters import CustomJsonFormatter
from dotenv import load_dotenv
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
env_debug = os.getenv('DEBUG', 'False')
if env_debug == 'False':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "apps.parser_habr",
    "apps.parser_tink",
    "apps.parser_mel",

    "rest_framework",
    'drf_spectacular',
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_prometheus.middleware.PrometheusAfterMiddleware'
]

ROOT_URLCONF = "parser.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "parser.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django_prometheus.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv('POSTGRES_DB', 'db'),
            "USER": os.getenv('POSTGRES_USER', 'postgres'),
            "PASSWORD": os.getenv('POSTGRES_PASSWORD', 'postgres'),
            "HOST": os.getenv('POSTGRES_HOST', 'localhost'),
            "PORT": os.getenv('POSTGRES_PORT', 5432),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CELERY_BEAT_SCHEDULE = {
      'pars-data-habr': {
        'task': 'apps.parser_habr.tasks.collect_data_habr',
        'schedule': crontab(minute='*/20'),
    },
    'pars-data-tinkoff': {
        'task': 'apps.parser_mel.tasks.collect_data_mel',
        'schedule': crontab(minute='*/20'),
    },
    'pars-data-mel': {
        'task': 'apps.parser_tink.tasks.collect_data_tinkoff',
        'schedule': crontab(minute='*/20'),
    },
}


CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '70/day',
        'user': '150/day'
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,

    'formatters': {
        'main_formatter': {
            'format': "{asctime} - {levelname} - {module} - {message}",
            "style": "{",
        },
        'json_formatter': {
              '()': CustomJsonFormatter,
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "main_formatter",
        },
        'file': {
                'class': 'logging.FileHandler',
                'filename': 'info.log',
                'formatter': 'json_formatter',
        }
    },

    "loggers": {
        "main": {
            "handlers": ["file", "console"],
            "propagate": True,
            "level": "INFO",
        },
    },
}

# Admin user

# abc2
# 123456789Rr
