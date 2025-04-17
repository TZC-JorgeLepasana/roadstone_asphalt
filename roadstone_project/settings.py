"""
Django settings for roadstone_project project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-secret-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.getenv('DEBUG', True)


# For development only (disable in production)
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1']
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Comment out muna


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'celery',
    'django_celery_beat',  # For scheduled tasks
    'channels',
    'django_celery_results',  # Optional: For storing task results in DB

    # Local apps
    'data_processing',
]

ASGI_APPLICATION = 'roadstone_project.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth backend
]


SITE_ID = 1

LOGIN_URL = 'login'  # URL to redirect to if user is not authenticated
LOGIN_REDIRECT_URL = 'home'  # URL to redirect to after successful login
LOGOUT_REDIRECT_URL = 'home'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'roadstone_project.urls'

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

WSGI_APPLICATION = 'roadstone_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Dublin'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Directories where Django will look for static files during development

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [BASE_DIR / "static"]

# Directory where Django will collect static files for production
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Celery Configuration (settings.py)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Dublin'

# Development-specific settings (override in production)
CELERY_WORKER_POOL = 'solo'  # Changed from gevent to solo for better debugging
CELERY_WORKER_CONCURRENCY = 1  # Easier to track tasks during development
CELERY_TASK_ALWAYS_EAGER = False  # Set to True for synchronous execution in tests

# Task visibility and state settings
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_SEND_SENT_EVENT = True  # Better task state visibility
CELERY_RESULT_EXTENDED = True  # Store more task state information

# Reliability settings (adjust for development)
CELERY_TASK_ACKS_LATE = False  # Disable for development to avoid ghost tasks
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_SOFT_TIME_LIMIT = 300  # 5 minutes soft limit
CELERY_TASK_TIME_LIMIT = 600  # 10 minutes hard limit

# Frontend integration settings
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True  # Auto-reconnect
CELERY_WORKER_SEND_TASK_EVENTS = True  # Enable events for monitoring

CELERY_BEAT_SCHEDULE = {
    'monitor-stalled-tasks': {
        'task': 'data_processing.tasks.monitor_stalled_tasks',
        'schedule': 300.0,  # Every 5 minutes
    },
}

PROCESSING_CHUNK_SIZE = 30
CACHE_LOCK_TIMEOUT = 60 * 5


# FTP Configuration (Use environment variables for sensitive data)
FTP_HOST = os.getenv('FTP_HOST', 'waws-prod-db3-169.ftp.azurewebsites.windows.net')
FTP_USER = os.getenv('FTP_USER', 'tzcftp\\tzcftp2')
FTP_PASS = os.getenv('FTP_PASS', 'M6@yPcCldNWXsmoyW')
FTP_PORT = int(os.getenv('FTP_PORT', 21))  # Default FTP port
REMOTE_DIR = os.getenv('REMOTE_DIR', '/site/wwwroot/ArchiveFiles/Roadstone Galway')

# Priority Metrics API
PRIORITY_METRICS_API_KEY = os.getenv('PRIORITY_METRICS_API_KEY', 'og3jhZwwK5880')  # Default for dev



# XML Upload Folder
XML_UPLOAD_FOLDER = os.path.join(MEDIA_ROOT, 'xml_uploads')
os.makedirs(XML_UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
