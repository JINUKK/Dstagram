"""
Django settings for config project.

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
SECRET_KEY = '#ivd*2rlr$(b2_4=*6ha^b*_4v=%pxpg@e#+k52iznn7j=j!lx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'photo',
    'disqus',
    'django.contrib.sites',
    'storages',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'layout')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AWS_ACCESS_KEY_ID = 'AKIA3XAZBG73E2HWYFUD'
AWS_SECRET_ACCESS_KEY = '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'

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'static.dstagram'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
# AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
AWS_S3_SECURE_URLS = True

AWS_S3_FILE_OVERWRITE = False
# True일 경우 같은 파일을 올렸을 때 덮어씌워진다.
# False를 하면 같은 파일이 올라와도 덮어씌워지지 않게 파일 이름을 자동으로 바꿔줌

# 브라우저가 해당 파일에 접속 했을 때 나타나는 파라미터 값
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# 지금올리는 파일의 권한을 지정해줌
AWS_DEFAULT_ACL = 'public-read'

AWS_LOCATION = ''

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'config.s3media.MediaStorage'

# MEDIA_URL = '/media/' # 가상 URL
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 루트 폴더를 만들어줌으로써 앞으로 사진을 찾을 때 MEDIA_ROOT 경로 아래에서만 찾게 할 수 있다.
# 루트 폴더가 자동으로 생김

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = '/'

from django.urls import reverse_lazy
LOGIN_URL = reverse_lazy('accounts:signin')

# django-disqus : 데이터베이스가 필요없음 -> disqus.com에서 관리함
# django.contrib.sites : 우리 프로젝트 사이트 정보 관리 -> python manage.py migrate를 해준다.
DISQUS_WEBSITE_SHORTNAME = 'koostargram'
SITE_ID = 1