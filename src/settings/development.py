# Part of settings for development environment.

from .base import *

INSTALLED_APPS += [
    'django_extensions'
]

SECRET_KEY = "not_secret"

DEBUG = 1

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "dev-chat.mszanowski.pl"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

# Django Rest Framework.

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += {
    # Allow default authentication classes to allow browsable API.
    # 'rest_framework.authentication.BasicAuthentication',
    # 'rest_framework.authentication.SessionAuthentication',
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


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_USE_TLS = True
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

ACCOUNT_EMAIL_VERIFICATION = 'none'