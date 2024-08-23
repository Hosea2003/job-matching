from .base import *

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
DEBUG = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "staticfiles"
