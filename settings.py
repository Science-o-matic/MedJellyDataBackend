# -*- coding: utf-8 -*-
import os

gettext = lambda s: s

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = "medjellydata.com"

ADMINS = (
    ('Martín Fuentes', 'fuentesmartin@gmail.com'),
    ('Antonio Barcia', 'antonio.barcia@gmail.com')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'mycms.db'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

STATIC_ROOT = 'static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0dasdsr6%7dasdsgip5tmez*vygfv+u14h@4lbt^8e2^26o#5_f_#b7%cm)u'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)


# i18n and l10n
LANGUAGES = (
    ('es', gettext('Español')),
)
DEFAULT_LANGUAGE = 0


ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
    'django_extensions',
    'tokenapi',
    'sights',
    'form_utils',
    'corsheaders',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'tokenapi.backends.TokenBackend'
)

TOKEN_TIMEOUT_DAYS = 1
TOKEN_CHECK_ACTIVE_USER = True

CORS_ORIGIN_ALLOW_ALL = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_SUBJECT_PREFIX = "[medjellydata] "
EMAIL_HOST = '<host>'
EMAIL_HOST_USER = '<user>'
EMAIL_HOST_PASSWORD = '<password>'
SERVER_EMAIL = "medjellydata@medjellydata.com"

MEDJELLY_API = {
    'debug': {
        'user': '<user>',
        'password': '<password>',
        'host': 'https://app.bahiasoftware.es/MEDUSAS/ws'
        },
    'production': {
        'user': '<user>',
        'password': '<password>',
        'host': 'https://app.bahiasoftware.es/MEDUSAS/ws'
        },
}

PROTECCION_CIVIL_API = {
    'base_url': 'https://www.googleapis.com/fusiontables/v1/query',
    'key': 'AIzaSyBSvPHuiAg_3D2Mzr1hy4rd78aIcX011s8',
    'tables': {
        'sightings': '1yYXZxBEPX6Tcwx2MKmLldCV1M2cvCqeXkYxxrhs',
        'beaches': '1T9Atse3TfuFEXqJKqMpDMS0gXkh05-hOPKTj47Y',
     }
}

LOGFILE = os.path.join(PROJECT_DIR, "logfile.log")

try:
    from local_settings import *
except ImportError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE,
            'maxBytes': 100000,
            'backupCount': 20,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
            }
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'sights': {
            'handlers': ['logfile', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
