import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


AWS_ACCESS_KEY_ID = get_env_variable("ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("SECRET_ACCESS_KEY")
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_STORAGE_BUCKET_NAME = get_env_variable("BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'config.settings.aws.utils.StaticRootS3BotoStorage'

DEFAULT_FILE_STORAGE = 'config.settings.aws.utils.MediaRootS3BotoStorage'
MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
