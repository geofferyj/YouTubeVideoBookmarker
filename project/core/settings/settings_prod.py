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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_PASSWORD = ''  
EMAIL_HOST_USER = ''  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  
