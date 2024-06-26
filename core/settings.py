# core/settings.py

import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="*") 

ADMIN_URL = env('DJANGO_ADMIN_URL', default="admin/")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'corsheaders',
    # Local
    'accounts.apps.AccountsConfig',
    'mastertheorem',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "static")],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database

POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_HOST = env.str("POSTGRES_HOST")

DATABASES = {
    "default": env.dj_db_url(
        "DATABASE_URL",
        default=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}",
    )
}

AUTH_USER_MODEL = "accounts.CustomUser"

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_FILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = env.bool("DJANGO_CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOW_CREDENTIALS = env.bool("DJANGO_CORS_ALLOW_CREDENTIALS", default=False)

# django-csp headers:

CSP_STYLE_SRC = (
    "'self'",
    "use.fontawesome.com",
    "cdnjs.cloudflare.com",
    "fonts.googleapis.com",
)

CSP_SCRIPT_SRC = ("'self'",)

CSP_IMG_SRC = (
    "'self'",
    "data:",
    "blob:",
)

CSP_FONT_SRC = (
    "'self'",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "data:",
)

CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = "'self'"
CSP_FORM_ACTION = ("'self'",)
CSP_INCLUDE_NONCE_IN = ("script-src", "style-src")
CSP_MANIFEST_SRC = ("'self'",)
CSP_WORKER_SRC = ("'self'",)
CSP_MEDIA_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_DEFAULT_SRC = ("'none'",)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://www.mastertheorem.io",
    "http://mastertheorem-aws-dev.us-west-2.elasticbeanstalk.com",
]


CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://www.mastertheorem.io",
    "http://mastertheorem-aws-dev.us-west-2.elasticbeanstalk.com",
]

# Production security settings

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)

SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)

CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
