"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from .secure_variables import EMAIL_PASSWORD,EMAIL_USER,TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_VERIFIED_NUMBER,_RAZOR_PAY_KEY_ID,_RAZOR_PAY_KEY_SECRET
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5#7-5(6om3vv*1r+x-_cjovk(y$*ey#&85zd&%dv&7!(x=5rk#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "verify_email.apps.VerifyEmailConfig",
    'django.contrib.humanize',
    'store',
    'accounts',
    'admincontrol',
    'categoryManagement',
    'product_management',
    'extra_management',
    'cart',
    'order',
    'wallet',
    'offer_management',
    'django_cleanup.apps.CleanupConfig',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.login_middleware.AdminLoginMiddleware',
]

ROOT_URLCONF = 'core.urls'
# Templates Directory
# TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'categoryManagement.context_processors.all_category',
                'categoryManagement.context_processors.all_atribute',
                'cart.context_processors.counter',
                'wallet.context_processors.wallet_balance',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'core/static',
]

#media file directory
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


#For To Enable Popus in Django or else it will block the payment popup
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.User'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOGIN_URL ='login-page'

HTML_MESSAGE_TEMPLATE ='accounts/send_verification_email_template.html'
VERIFICATION_SUCCESS_TEMPLATE ='accounts/email_verification_success.html'


# Settings for otp verification

ACCOUNT_SID= TWILIO_ACCOUNT_SID
AUTH_TOKEN=TWILIO_AUTH_TOKEN
COUNTRY_CODE='+91'
TWILIO_PHONE_NUMBER=TWILIO_VERIFIED_NUMBER


#settings for RazorPay
RAZORPAY_KEY_ID = _RAZOR_PAY_KEY_ID
RAZORPAY_KEY_SECRET = _RAZOR_PAY_KEY_SECRET