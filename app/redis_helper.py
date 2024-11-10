import redis
from config import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_USER

def check_redis_params():
    if REDIS_HOST is None:
        raise ValueError("REDIS_HOST is not set")
    if REDIS_PORT is None:
        raise ValueError("REDIS_PORT is not set")
    if REDIS_DB is None:
        raise ValueError("REDIS_DB is not set")
    if REDIS_PASSWORD is None:
        raise ValueError("REDIS_PASSWORD is not set")
    if REDIS_USER is None:
        raise ValueError("REDIS_USER is not set")
    return True

def get_redis_connection():
    if not check_redis_params():
        return None
    return redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        username=REDIS_USER
    )

