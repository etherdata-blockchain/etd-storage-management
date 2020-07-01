"""
Django settings for serverless project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y#n2o@b)bu#cu7khqm7x21fwh7t38i-cv+*-6w-@3x6f8cg((#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "corsheaders",
    "storage_management",
    'django_filters',
    "django_cleanup.apps.CleanupConfig",
    "drf_auto_endpoint"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'serverless.urls'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

DRF_AUTO_METADATA_ADAPTER = 'drf_auto_endpoint.adapters.EmberAdapter'

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

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

WSGI_APPLICATION = 'serverless.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': '../serverless.db',
        "ENGINE": "django.db.backends.sqlite3",
        "CHARSET": "utf8",
        "COLLATION": "utf8_general_ci"
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_METADATA_CLASS': 'drf_auto_endpoint.metadata.MinimalAutoMetadata',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_STORAGE_BUCKET_NAME = "storage-management-data"
#
AWS_DEFAULT_ACL = None
#
AWS_S3_REGION_NAME = "ap-northeast-1"

MEDIAFILES_LOCATION = 'media'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

AWS_S3_CUSTOM_DOMAIN = 'storage.sirileepage.com'

# AWS_LOCATION = "static"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATIC_URL = '/static/'

# MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, "media")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
