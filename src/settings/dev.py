# Part of settings for development environment.

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

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