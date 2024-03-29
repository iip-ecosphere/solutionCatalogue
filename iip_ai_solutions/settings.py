"""
Django settings for iip_ai_solutions project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

from .env import ENV_STR, ENV_BOOL, ENV_INT, ENV_LIST

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_STR("SECRET_KEY", "insecurekey")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_STR("SECRET_KEY") is None

ALLOWED_HOSTS = ENV_LIST("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

SECURE_SSL_REDIRECT = ENV_BOOL("SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = DEBUG
SESSION_SAVE_EVERY_REQUEST = True

# Application definition

INSTALLED_APPS = [
    "catalogue.apps.CatalogueConfig",
    "cms.apps.CmsConfig",
    "grappelli",
    "nested_admin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "debug_toolbar",
    "django_sass",
    "bulma",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.gitlab",
    "allauth.socialaccount.providers.twitter",
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "iip_ai_solutions.urls"

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
                "django.template.context_processors.request",
                "catalogue.context.base_context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "iip_ai_solutions.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

GRAPPELLI_ADMIN_TITLE = "Admin - KI-Lösungskatalog - IIP-Ecosphere"
GRAPPELLI_SWITCH_USER = True

INTERNAL_IPS = [
    "127.0.0.1",
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = LOGOUT_REDIRECT_URL
LOGIN_URL = "/accounts/login/"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = not DEBUG
ACCOUNT_EMAIL_VERIFICATION = ENV_STR(
    "ACCOUNT_EMAIL_VERIFICATION", "optional" if DEBUG else "mandatory"
)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": ENV_STR("SOCIAL_GITHUB_CLIENT_ID", ""),
            "secret": ENV_STR("SOCIAL_GITHUB_SECRET", ""),
            "key": "",
        }
    },
    "gitlab": {
        "APP": {
            "client_id": ENV_STR("SOCIAL_GITLAB_CLIENT_ID", ""),
            "secret": ENV_STR("SOCIAL_GITLAB_SECRET", ""),
            "key": "",
        }
    },
    "twitter": {
        "APP": {
            "client_id": ENV_STR("SOCIAL_TWITTER_CLIENT_ID", ""),
            "secret": ENV_STR("SOCIAL_TWITTER_SECRET", ""),
            "key": "",
        }
    },
}

SENDER_EMAIL_MESSAGE = ENV_STR("SENDER_EMAIL_MESSAGE", "noreply@example.com")
SENDER_EMAIL_FEEDBACK = ENV_STR("SENDER_EMAIL_FEEDBACK", "noreply@example.com")
SENDER_EMAIL_APPROVE = ENV_STR("SENDER_EMAIL_APPROVE", "noreply@example.com")
EMAIL_HOST = ENV_STR("EMAIL_HOST", "localhost")
EMAIL_PORT = ENV_INT("EMAIL_PORT", 1025)
EMAIL_HOST_USER = ENV_STR("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = ENV_STR("EMAIL_HOST_PASSWORD", "")

CKEDITOR_CONFIGS = {
    "component": {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            [
                "Bold",
                "Italic",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink"],
            ["NumberedList", "BulletedList", "Table"],
            ["Source"],
        ],
        "toolbar": "Full",
        "removePlugins": "stylesheetparser",
        "allowedContent": "p h b ul ol li i dl em table tr th td a[*]{*}(*)",
    },
    "cms": {"extraAllowedContent": "div(*)"},
    "default": {},
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True
