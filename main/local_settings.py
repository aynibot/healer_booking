
CHANNEL_ID = '1603100301'
CHANNEL_SECRET = '814c0d391f96a99bb1595ca492db1167'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://h:pb881cf92e6fa53cf0dc4bb9210b608f4120df8452b5e0f913318dde7fa6c9624@ec2-18-209-218-148.compute-1.amazonaws.com:58689',
        "OPTIONS": {
            'max_connections': 20,
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "ayni"
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dr8d4u3hlegab',
        'USER': 'jlgkcurudzrhhn',
        'PASSWORD': '3f0d25ec805aa01a700a80856c63d11f38df88d58add2710d1ae0ff6a17cfb96',
        'HOST': 'ec2-54-163-246-5.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}