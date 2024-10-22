from pathlib import Path
from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASE_URL = config(option='BASE_URL', default=None)

# Default email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config(option='EMAIL_HOST', cast=str, default=None)
EMAIL_PORT = config(option='EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = config(option='EMAIL_HOST_USER', cast=str, default=None)
EMAIL_HOST_PASSWORD = config(option='EMAIL_HOST_PASSWORD', cast=str, default=None)
EMAIL_USE_TLS = config(option='EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_USE_SSL = config(option='EMAIL_USE_SSL', cast=bool, default=False)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Setting admins and managers
ADMIN_NAMES = config(option='ADMIN_NAMES', cast=Csv(), default='')
ADMIN_EMAILS = config(option='ADMIN_EMAILS', cast=Csv(), default='')
ADMINS = list(zip(ADMIN_NAMES, ADMIN_EMAILS)) if ADMIN_NAMES and ADMIN_EMAILS else list()
MANAGERS = ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(option='DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config(option='DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.railway.app'] if DEBUG else ['.railway.app']

CSRF_TRUSTED_ORIGINS = ['http://*.127.0.0.1', 'http://*.localhost', 'https://*.railway.app'] if DEBUG else ['https://*.railway.app']

# Application definition
STARTED_APPS = [
    'visits',
    'console',
    'subscriptions',
    'customers',
    'checkouts',
    'generative',
    'landing',
]

# Vendor apps definition
VENDOR_APPS = [
    "allauth_ui",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    "widget_tweaks",
    'slippers',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *STARTED_APPS,
    *VENDOR_APPS,
]


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
    'console.utils.middleware.subscription.SubscriptionMiddleware',
    'console.utils.middleware.profile.ProfileMiddleware'
]

ROOT_URLCONF = 'sora.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'console.utils.templates.context_processors.augmentation'
            ],
        },
    },
]

WSGI_APPLICATION = 'sora.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DB_CONN_MAX_AGE = config(option='CONN_MAX_AGE', cast=int, default=30)
DB_CONN_STRR = config(option='DB_CONN_STRR', default=None)


if DB_CONN_STRR:
    import dj_database_url
    DATABASES['default'].update(
       dj_database_url.config(
            default=DB_CONN_STRR,
            conn_max_age=DB_CONN_MAX_AGE,
            conn_health_checks=True
        )
   )


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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

]

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user:email',
        ],
    }
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION='mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX='Sora'
ACCOUNT_EMAIL_REQUIRED=True

ACCOUNT_FORMS = {'login': 'console.utils.forms.subscriptions.forms.CustomLoginForm',
                 'signup': 'console.utils.forms.subscriptions.forms.CustomSignUpForm',
                 'change_password': 'console.utils.forms.subscriptions.forms.CustomChangePasswordForm'}
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage', 
    },
}