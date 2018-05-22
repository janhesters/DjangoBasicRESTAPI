from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('POSTGRES_NAME'),
        'USER': get_env_variable('POSTGRES_USERNAME'),
        'PASSWORD': get_env_variable('POSTGRES_PASSWORD'),
        'HOST': get_env_variable('POSTGRES_HOST'),
        'PORT': get_env_variable('POSTGRES_PORT'),
    }
}

STATIC_URL = '/static/'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Media files

MEDIA_ROOT = BASE_DIR.parent / 'myproject' / 'media'


# Security settings


SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SECURE_SSL_HOST = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_CONTENT_TYPE_NOSNIFF = False
