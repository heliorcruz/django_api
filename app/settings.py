import os
import django_heroku

import environ
# Load operating system env variables and prepare to use them
env = environ.Env()

# local.env file, should load only in development environment
env_file = os.path.join(os.path.dirname(__file__), 'local.env')
if os.path.exists(env_file):
    environ.Env.read_env(str(env_file))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env('DJANGO_SECRET_KEY', default='hgFˆ&8iJBvfTˆ&8oKJBVdRTuiJRuIJhtghJIyTRfUJbvDRtyU')

#SECRET_KEY = 'hgFˆ&8iJBvfTˆ&8oKJBVdRTuiJRuIJhtghJIyTRfUJbvDRtyU'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
# ALLOWED_HOSTS = ['127.0.0.1']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_yasg',
]

PROJECT_APPS = [
    'users',
    'articles',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },

    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database

DATABASES = {
    'default': env.db('DATABASE_URL')  
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
}]

# Authentication

AUTH_USER_MODEL = 'users.User'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static (CSS, JavaScript, Images) and Media (uploads) files

STATIC_ROOT = os.path.join(BASE_DIR, '.static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '.media')
MEDIA_URL = 'media/'

# Email settings

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'no-reply@localhost'

# Activate Django-Heroku.
django_heroku.settings(locals())
