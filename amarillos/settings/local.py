from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

from dotenv import load_dotenv
import os

load_dotenv()

STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
EMAIL_TO_DEBUG = ["axjugoma@gmail.com"]
ALLOWED_HOSTS = ["localhost","127.0.0.1","192.168.10.146","adosistemas2023.pythonanywhere.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'amarillos',
        'USER': 'root', 
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',   #my port is 3306
        'OPTIONS':{
            'read_default_file': '/opt/lampp/etc/my.cnf',
        }
    }
}