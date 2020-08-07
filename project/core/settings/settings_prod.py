from .base import *

DEBUG = False 

ALLOWED_HOSTS = ['localhost', 'handsfreeyoutube.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'handsfreeyoutube_db',
        'USER': 'project_admin',
        'PASSWORD': 'project_admin_password_#001',
        'HOST': 'localhost',
        'PORT': '',
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')