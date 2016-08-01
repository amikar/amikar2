import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'NAME': 'websql2',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '1',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}

DEBUG = True