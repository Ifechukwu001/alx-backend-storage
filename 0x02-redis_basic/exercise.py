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

    def get(self, key: str, fn: typing.Callable) -> typing.Union[
                                                                str,
                                                                bytes,
                                                                int,
                                                                float]:
        """Gets a data stored at a key.

        Args:
            key (str): Key used to store the data.
            fn (typing.Callable): Callback function to render
                                the returned data in the right format.

        Returns:
            typing.Union[str, bytes, int, float]: Stored data.
        """
        data: bytes = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Gets data stored at key as a string.

        Args:
            key (str): Key used to store the data.

        Returns:
            str: String data.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Gets data stored at key as an Integer.

        Args:
            key (str): Key used to store the data.

        Returns:
            int: Integer data.
        """
        return self.get(key, int)
