import redis

from phishield.conf import environment


def get_cache():
    return redis.from_url(environment.CACHE_URI, decode_responses=True)
