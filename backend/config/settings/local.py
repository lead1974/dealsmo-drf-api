from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-k8^yl6j_k=)6#^+k_+&!5=yt^rj-8*-l+l^)k7h+juy7qj#)v$",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Frontend URL for local development
FRONTEND_URL = env.str('FRONTEND_URL', default='http://localhost:8080')

# OAuth settings for local development
OAUTH_CALLBACK_DOMAIN = env.str('OAUTH_CALLBACK_DOMAIN', default=FRONTEND_URL)
GOOGLE_OAUTH_CALLBACK_URL = f"{OAUTH_CALLBACK_DOMAIN}/api/v1/auth/social/google/callback/"

# CORS settings for local development
CORS_ORIGIN_WHITELIST = [FRONTEND_URL]
CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
EMAIL_PORT = env("EMAIL_PORT", default=1025)
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="DealsMo <noreply@delasmo.com>")
DOMAIN = env("DOMAIN", default="localhost:8080")
SITE_NAME = env("SITE_NAME", default="DealsMo.com")


CELERY_BROKER_URL = env("CELERY_BROKER", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")

CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_EXCHANGE = "default"
