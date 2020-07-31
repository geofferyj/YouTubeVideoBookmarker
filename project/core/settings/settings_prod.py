from .base import *

DEBUG = False 

ALLOWED_HOSTS = ['web']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'),] 
GOOGLE_RECAPTCHA_SECRET_KEY = '6LcxrbAZAAAAAKhbc1l1IKfQ_OJ2MSlh1No79giD'