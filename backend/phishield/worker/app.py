import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AsyncIO, Retries
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

from phishield.conf import environment
from phishield.packages.dramatiq.middlewares.status import Status



broker = RedisBroker(host=environment.CACHE_HOST)
results = RedisBackend(host=environment.CACHE_HOST, namespace="phishield-results")
status = RedisBackend(host=environment.CACHE_HOST, namespace="phishield-status")

broker.add_middleware(AsyncIO())
broker.add_middleware(Retries())
broker.add_middleware(Results(backend=results))
broker.add_middleware(Status(backend=status), before=Retries)
dramatiq.set_broker(broker)