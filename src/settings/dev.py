# Part of settings for development environment.

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += {
    # Allow default authentication classes to allow browsable API.
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
}