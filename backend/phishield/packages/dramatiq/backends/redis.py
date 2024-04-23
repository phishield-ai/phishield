import hashlib

from dramatiq.results.backends import RedisBackend as BaseRedisBackend


class RedisBackend(BaseRedisBackend):
    """
    Custom RedisBackend that allows the message result to be found on
    the backend only by the message_id and namespace, without having
    to know the queue name and actor name.
    """

    def build_message_key(self, message) -> str:
        message_key = "%(namespace)s:%(message_id)s" % {
            "namespace": self.namespace,
            "message_id": message.message_id,
        }
        return hashlib.md5(message_key.encode("utf-8")).hexdigest()
