from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
from dotenv import load_dotenv
import os

load_dotenv()

# STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static"),)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEBUG = True
ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS.extend(filter(None,os.environ.get("ALLOWED_HOSTS",'').split(',')))
PROCESA_FTP = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adosistemas2023$amarillos',
        'USER': 'adosistemas2023',
        'PASSWORD': 'T3l3f0n0*',
        'HOST': 'adosistemas2023.mysql.pythonanywhere-services.com',
        'PORT': '3306',   #my port is 3306
        'OPTIONS':{
            'read_default_file': '/opt/lampp/etc/my.cnf',
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}