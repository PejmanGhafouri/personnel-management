import json
import os
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()
environ.Env.read_env()


def get_env_value(env_variable, default_value=None):
    try:
        return env.get_value(env_variable)
    except KeyError:
        if default_value:
            return default_value
        else:
            error_msg = 'Please set the {} environment variable'.format(env_variable)
            raise ImproperlyConfigured(error_msg)


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_env_value('SECRET_KEY')

DEBUG = json.loads(get_env_value('DEBUG', False))

ALLOWED_HOSTS = get_env_value('ALLOWED_HOSTS', '*').replace(', ', ',').replace(' ,', ',').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'apps.user.apps.UserConfig',
    'apps.personnel.apps.PersonnelConfig',
    'main_app',
    'apps.iranian_cities',
    'django_crontab',
    'widget_tweaks',
    'django_node_assets',
    'jalali_date',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'main_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_value('DB_NAME'),
        'USER': get_env_value('DB_USER'),
        'PASSWORD': get_env_value('DB_PASSWORD'),
        'HOST': get_env_value('DB_HOST'),
        'PORT': get_env_value('DB_PORT'),
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': get_env_value('REDIS_LOCATION'),
    }
}

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

LANGUAGE_CODE = 'fa-IR'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'node_modules'),
]

# Django Node Assets Config
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_node_assets.finders.NodeModulesFinder',
]
NODE_PACKAGE_JSON = './package.json'
NODE_MODULES_ROOT = './node_modules'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Default user model
AUTH_USER_MODEL = 'user.User'

LOGIN_REDIRECT_URL = 'user:send-sms'
DASHBOARD_REDIRECT_URL = 'personnel:dashboard'

# Kavenegar Config
KAVENEGAR_KEYAPI = get_env_value('KAVENEGAR_KEYAPI')
SENDER_NUMBER = get_env_value('SENDER_NUMBER')

# Crontab Config
CRONJOBS = [
    ('*/1 * * * *', 'apps.personnel.cron.expired_contract_demand')  # Every 1 min
]

# django jalali date settings

JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}
