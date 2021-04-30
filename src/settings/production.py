# Part of settings for production environment.

from .base import *

SECRET_KEY = "not_secret"

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost', 'chat.mszanowski.pl']