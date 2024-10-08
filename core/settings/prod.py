from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "staticfiles"

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://18.216.218.232"]
