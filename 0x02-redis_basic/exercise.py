#!/usr/bin/env python3
"""Redis on Python

"""
import redis
import typing
import uuid


class Cache:

    def __init__(self) -> None:
        """Initialize the Cache instance.

        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """Stores input data in redis

        Args:
            data (typing.Union[str, bytes, int, float]): Input data.

        Returns:
            str: Key used to store the data.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
