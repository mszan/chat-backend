# Part of settings for development environment.

from .base import *

SECRET_KEY = "not_secret"

DEBUG = 1

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chat_backend',
        'USER': 'chat_backend_user',
        'PASSWORD': 'Test@1234',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Django Rest Framework.

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += {
    # Allow default authentication classes to allow browsable API.
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
}

# Django Cors Headers.

CORS_ORIGIN_ALLOW_ALL = True    # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect.
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3030',
# ]   # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`.
# CORS_ORIGIN_REGEX_WHITELIST = [
#     'http://localhost:3030',
# ]
