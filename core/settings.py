
import os
from decouple import config 
from pathlib import Path
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

GEMINI_API_KEY = config("GEMINI_API_KEY")
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_PUBLIC_KEY')
MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_ACCESS_TOKEN')


ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY')





SITE_ID = 1
DJANGO_APPS = [
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'olo',
    'user',
    'product',
    'perfil'
          
]

THIRD_PARTY_APPS = [
 
    'rest_framework',
    'corsheaders', 
    'rest_framework_simplejwt',

   
   
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
DATABASES['default']['ATOMIC_REQUESTS'] =True


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'es-ar' 
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True 

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
   
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10, 
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


FRONTEND_URLS = config('FRONTEND_URL', default='http://localhost:3000')

CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in FRONTEND_URLS.split(',')
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in FRONTEND_URLS.split(',')
]

#CORS_ALLOW_ALL_ORIGINS = False
#CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DESTINATION_EMAIL = config('DESTINATION_EMAIL', default=EMAIL_HOST_USER)


AUTH_USER_MODEL = 'user.UserAccount'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# settings.py

# 1. Configuramos las rutas locales de media (ESTO ES VITAL)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 2. Tu lógica de Storage ajustada para local
GS_BUCKET_NAME = config('GS_BUCKET_NAME', default='')

# Solo activamos Google Cloud si hay un bucket y NO estamos en DEBUG (local)
if GS_BUCKET_NAME and not DEBUG:
    google_creds = config('GOOGLE_APPLICATION_CREDENTIALS', default='')
    
    if google_creds.startswith('{'):
        credenciales_path = os.path.join(BASE_DIR, 'google-creds-temp.json')
        with open(credenciales_path, 'w') as archivo:
            archivo.write(google_creds)
    else:
        credenciales_path = os.path.join(BASE_DIR, google_creds)
        
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credenciales_path
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # 🏠 CONFIGURACIÓN PARA DESARROLLO LOCAL
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
