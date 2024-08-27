from .base import *

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
DEBUG = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "staticfiles"
