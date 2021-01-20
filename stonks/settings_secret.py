SECRET_KEY = ''

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stonksDB',
        'USER': 'username',
        'PASSWORD': 'password-change',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
