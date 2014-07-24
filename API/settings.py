"""
Django settings for API project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UX_DB_NAME = os.environ.get("UX_DB_NAME")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ao3#c802%*%gi^*r_1wpnl=mz%q+yp)ht0at*gjd*2h51b7k_e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'formAPI',
    'rest_framework.authtoken',
    'corsheaders',
    "djrill",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'API.urls'

WSGI_APPLICATION = 'API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["UX_DB_NAME"],
        'USER': os.environ["UX_DB_USER"],
        'PASSWORD': os.environ["UX_DB_PASSWORD"],
        'HOST': os.environ["UX_DB_HOST"],
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# REST_FRAMEWORK = {
#     'PAGINATE_BY': 3
# }

"""EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'DX.LAB@gmail.com'
EMAIL_PORT = 25"""
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'uxlab.nerd.1@gmail.com'
# EMAIL_HOST_PASSWORD = 'uxlabnerd1'
DEFAULT_FROM_EMAIL = "uxlab.nerd.1@gmail.com"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
MANDRILL_API_KEY = "swhhK5l8hMDLIhjlveU0Pg"

{
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
REST_FRAMEWORK = {
    #Comment to remove pagination
    'PAGINATE_BY': 3,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/minute',
        'user': '10000/minute'
    },
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #leaving this in for now so we can use the API
        'rest_framework.authentication.SessionAuthentication',
        'formAPI.tokenAuth.ExpiringTokenAuth',
    )
}

CORS_ORIGIN_ALLOW_ALL = True
