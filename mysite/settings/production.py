from .base import *
import os
import dj_database_url

DEBUG = False

# Fetch secret key from environment variable
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Allowed hosts from environment variable (comma-separated list)
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# CSRF settings for production (IMPORTANT for Wagtail with Cloudflare)
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# Database Configuration
# If DATABASE_URL is set in .env (e.g. postgres://user:pass@host/db), use it.
# Otherwise, fall back to the default SQLite defined in base.py
db_from_env = dj_database_url.config(conn_max_age=600)
if db_from_env:
    DATABASES['default'].update(db_from_env)

# WhiteNoise Configuration for Static Files
STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

# Cloudflare R2 (S3 Compatible Storage) Configuration for Media
AWS_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
AWS_S3_REGION_NAME = "auto"
AWS_S3_CUSTOM_DOMAIN = os.getenv("R2_CUSTOM_DOMAIN")

STORAGES["default"] = {
    "BACKEND": "storages.backends.s3.S3Storage",
    "OPTIONS": {
        "location": "media",
    }
}

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

try:
    from .local import *
except ImportError:
    pass
