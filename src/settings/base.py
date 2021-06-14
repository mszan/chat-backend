from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sites',

    # Third-party libraries.
    'rest_framework',
    'drf_api_logger',
    'corsheaders',
    'channels',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Django apps.
    'api'
]

MIDDLEWARE = [
    # Django Cors Headers.
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Django Rest Framework Logger.
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates')
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model.

AUTH_USER_MODEL = "api.CustomUser"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('static')

# Django Rest Framework.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

# Django Rest Framework Logger.

DRF_API_LOGGER_DATABASE = True    # Enable logging into database table.

# Django Channels.

ASGI_APPLICATION = "api.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# JWT_AUTH = {
#     'JWT_ALLOW_REFRESH': True
# }

# should not work due to https://django-rest-auth.readthedocs.io/en/latest/installation.html#jwt-support-optional
REST_USE_JWT = True