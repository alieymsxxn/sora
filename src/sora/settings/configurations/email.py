from decouple import config
# Default email backend
email_configurations = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': config(option='EMAIL_HOST', cast=str, default=None),
    'EMAIL_PORT': config(option='EMAIL_PORT', cast=int, default=587),
    'EMAIL_HOST_USER': config(option='EMAIL_HOST_USER', cast=str, default=None),
    'EMAIL_HOST_PASSWORD': config(option='EMAIL_HOST_PASSWORD', cast=str, default=None),
    'EMAIL_USE_TLS': config(option='EMAIL_USE_TLS', cast=bool, default=True),
    'EMAIL_USE_SSL': config(option='EMAIL_USE_SSL', cast=bool, default=False),
    'DEFAULT_FROM_EMAIL': config(option='EMAIL_HOST_USER', cast=str, default=None),
    'SERVER_EMAIL': config(option='EMAIL_HOST_USER', cast=str, default=None),
}