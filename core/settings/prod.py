from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "staticfiles"
