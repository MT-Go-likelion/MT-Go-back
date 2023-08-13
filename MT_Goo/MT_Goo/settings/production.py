from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')