"""
Django settings for example project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&+gxvnt5hnb^ginv90(@hx_gn+8&42y511(&)6vif25^$&tzl$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_flickr_gallery',

    'example.myapp',

    # ckeditor
    'ckeditor',
    'ckeditor_uploader',
    'flickr_ckeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'example.example.urls'

WSGI_APPLICATION = 'example.example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'gallery.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# The docs say it should be absolute path: BASE_DIR is precisely one.
# Life is wonderful!
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# flickr settings
# https://github.com/arkanister/django-flickr-gallery

FLICKR_API_KEY = os.environ['FLICKR_API_KEY']
FLICKR_SECRET = os.environ['FLICKR_SECRET']
FLICKR_USER_ID = os.environ['FLICKR_USER_ID']


# ckeditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_MyToolbar': [
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],
            ['Undo', 'Redo'],
            ['Scayt'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flickr', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Source'],
            ['Maximize', 'ReadMore'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike',
            'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-',
            'Outdent', 'Indent', '-', 'Blockquote'],
            ['Styles', 'Format'],
        ],
        'extraPlugins': 'flickr',
        'toolbar': 'MyToolbar',
    },
}
