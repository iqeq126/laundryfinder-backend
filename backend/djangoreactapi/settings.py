"""
Django settings for djangoreactapi project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os.path, datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False
# ALLOWED_HOSTS = ['172.19.97.162']
ALLOWED_HOSTS = ['127.0.0.1', '172.19.86.24', '172.19.87.20', '192.168.1.13', '138.2.117.158','192.168.0.2', 'localhost']
# ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "crud",
    "post",  # 추가
    "tag",
    "user",
    "ptfile",
    "rest_framework",  # 추가
    "corsheaders",  # 추가
    'rest_framework_swagger',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'ocr',
    # simple-jwt 추가해주기
    # 로그인 관련
    'rest_framework.authtoken',
    'django.core.files.storage',
    #'dj_rest_auth',
    #'django.contrib.sites',
    
    #'allauth',
    #'allauth.account',
    # 'dj_rest_auth.registration',
    # 태그 관련
    #'blog.apps.BlogConfig',
    #'taggit.apps.TaggitAppconfig',
    #'taggit_templatetags2',
    #'taggit',
    ##############
]
# 다중 이미지 업로드
MEDIA_URL = '/images/'
MEDIA_ROOT = 'C:/NAS/Frontend/frontend/public/images/'


#로그인 관련#########
AUTH_USER_MODEL = 'user.User'
#REST_USE_JWT = True
#JWT_AUTH_COOKIE = 'my-app-auth'
#JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'

SITE_ID = 1
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
###############
# 태그 관련
# TAGGIT_CASE_INSENSITIVE = True
# TAGGIT_LIMIT = 50
########
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 추가
    "django.middleware.common.CommonMiddleware",  # 추가
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangoreactapi.urls"

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = (
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://172.19.87.20:8000',
    'https://172.19.87.20:3000',
    'http://172.19.86.24:8000',
    'https://172.19.86.24:3000',
    'http://192.168.0.2:8000',
    'https://192.168.0.2:3000',
    'https://localhost:3000',
    'https://127.0.0.1:3000',
    'http://138.2.117.158',
    'https://192.168.1.13:3000',
    'http://192.168.1.13:8000'
)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'

CORS_ORIGIN_WHITELIST = [
    "https://api.openweathermap.org",
    "http://apis.data.go.kr",
    "http://172.19.87.20:8000",
    "https://172.19.87.20:3000",
    "http://172.19.86.24:8000",
    "https://172.19.86.24:3000",
    "http://192.168.0.2:8000",
    "https://192.168.0.2:3000",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://172.19.97.162:8000",
    'http://138.2.117.158',
    "https://api.ocr.space",
    'https://192.168.1.13:3000',
    'http://192.168.1.13:8000',
    #"//dapi.kakao.com/v2/maps/sdk.js?",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'frontend', 'build'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crud', 'static')
]
WSGI_APPLICATION = "djangoreactapi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "web",
        "USER": "user",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "3309",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [ # 기본적인 view 접근 권한 지정
        'rest_framework.permissions.AllowAny'
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [  # session 혹은 token을 인증 할 클래스 설정
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': [  # request.data 속성에 액세스 할 때 사용되는 파서 지정
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ]
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# 로그인 관련
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'login_id',
    'USER_ID_CLAIM': 'login_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}
##############
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
