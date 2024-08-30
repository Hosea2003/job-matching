from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "staticfiles"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    f"http://{os.getenv("ALLOWED_HOST")}"
]
