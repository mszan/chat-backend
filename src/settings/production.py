# Part of settings for production environment.

from .base import *

SECRET_KEY = "not_secret"

DEBUG = 1

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "51.195.101.186", "chat.mszanowski.pl"]

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