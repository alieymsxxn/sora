from .base import *

# collectstatic will accumulate staticfiles here
STATIC_ROOT = BASE_DIR / 'local-cdn'
# URL used to refer staticfiles inside STATIC_ROOT
STATIC_URL = 'static/'
# Generated path for collectstatic to look for staticfiles
STATICFILES_BASE_DIR = BASE_DIR / 'staticfiles'
STATICFILES_BASE_DIR.mkdir(parents=True, exist_ok=True)
# Defining source(s) for python manage.py collectstatic to collect from
STATICFILES_DIRS = [ STATICFILES_BASE_DIR ]
# Generated path for vendor, custom staticfiles for custom usage
STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / 'vendors'
STATICFILES_CUSTOM_DIR = STATICFILES_BASE_DIR / 'assets'
# Backends that define where to find staticfiles from
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
