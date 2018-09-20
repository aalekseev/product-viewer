# coding: utf-8
from typing import Iterator, Tuple, List

import redis

from product_viewer.settings import SETTINGS

YML_PREFIX = 'yml-offer_'
# Multiple values stored in one string
# separated with separator
SEPARATOR = ': '


class RedisStore:
    """Responsible for interaction with Redis store."""

    def __init__(self):
        self.cursor = redis.StrictRedis(
            host=SETTINGS.value('redis/host', 'localhost', str),
            port=SETTINGS.value('redis/port', '6379', str),
            db=SETTINGS.value('redis/db', '0', str),
        )

    def load(self) -> Iterator[List]:
        """Loads all values associated with prefix."""

        for key in self.cursor.scan_iter(YML_PREFIX + '*'):
            yield self.cursor.get(key).decode('utf-8').split(SEPARATOR)

    def dump(self, key: str, val: Tuple[str]):
        """Stores key and value."""

        self.cursor.set(YML_PREFIX + str(key), SEPARATOR.join(val))
