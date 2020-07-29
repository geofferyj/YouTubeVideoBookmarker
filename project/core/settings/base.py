import os  

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = 'g3wxnr5%u=w@!+lfoy+xdq@813p-4p@gfaoz5tuma=-2z@*p@0'
# SECRET_KEY = os.getenv('MYSITE_SECRET_KEY', '')


INSTALLED_APPS = [
    'django.contrib.admin',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_inlinecss',
    'crispy_forms',
    'bookmarker',
    'user_profile',
    'promo_code',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID =1

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

YOUTUBE_DATA_API_KEY = 'AIzaSyBnD826tz_SelYOn6FtJHGPeGqMMKiIjuI'
# LOGIN_REDIRECT_URL = 'admin_page'
# LOGOUT_REDIRECT_URL = 'index'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# LOGIN_URL = 'login'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_PASSWORD = 'blessing okot'  
EMAIL_HOST_USER = 'geofferyjoseph1@gmail.com'  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  

# ---------------- allauth settings -------------------#

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=7

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "optional"

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5

ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400

ACCOUNT_LOGOUT_REDIRECT_URL = 'index'

# LOGIN_REDIRECT_URL = 'index'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

AUTH_USER_MODEL = 'bookmarker.User'