# Part of settings for production environment.

from .base import *
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# TODO: Make this false.
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost', 'chat-app.mszanowski.pl']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://chat-app.mszanowski.pl"
]
