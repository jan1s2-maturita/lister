import os

DEBUG = True

PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH')
REDIS_HOST = 'redis' if DEBUG else os.environ.get('REDIS_HOST')
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_USER = 'redis_user' if DEBUG else os.environ.get('REDIS_USER')
REDIS_PASSWORD = 'redis_password' if DEBUG else os.environ.get('REDIS_PASSWORD')

