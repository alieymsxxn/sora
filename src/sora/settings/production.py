from .base import *

# Setting compatible sqlite version for Chromadb
if not DEBUG:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Overriding storages for production
STORAGES = { }

# AWS IAM Credentials
AWS_ACCESS_KEY_ID = config(option='AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config(option='AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config(option='AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config(option='AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = config(option='AWS_S3_CUSTOM_DOMAIN')


# URL used to refer staticfiles inside STATIC_ROOT
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
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
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
]

# Opting for S3Boto3Storage to collect staticfiles on S3
STORAGES.update({
    'staticfiles': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage', 
        }
    })
