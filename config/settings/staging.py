from .aws.conf import *
from .base import *

DEBUG = True

# TODO: Add your list of allowed hosts
ALLOWED_HOSTS = []

INSTALLED_APPS += ['storages', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('RDS_DB_NAME'),
        'USER': get_env_variable('RSD_USERNAME'),
        'PASSWORD': get_env_variable('RDS_PASSWORD'),
        'HOST': get_env_variable('RDS_HOSTNAME'),
        'PORT': get_env_variable('RDS_PORT'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_env_variable('REDIS_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_SSL_HOST = True
# TODO: CHANGE THIS TO A YEAR ONCE YOUR ARE READY! 5 minutes for testing.
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# Set this one up for some PaaS. E.g. Heroku needs it.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
