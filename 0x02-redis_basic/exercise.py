#!/usr/bin/env python3
"""Redis on Python

"""
import redis
import typing
import uuid
import functools


def count_calls(method: typing.Callable) -> typing.Callable:
    """Counts times a method is called

    Args:
        method (typing.Callable): Method to be counted.

    Returns:
        typing.Callable: Inner function.
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]
        key = method.__qualname__
        self._redis.incr(key)
        return method(*args, **kwargs)

    return wrapper


def call_history(method: typing.Callable) -> typing.Callable:
    """Saves the input and output data.

    Args:
        method (typing.Callable): Method call to save.

    Returns:
        typing.Callable: Inner function.
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]
        self._redis.rpush(
                            "{}:inputs".format(method.__qualname__),
                            str(args[1:])
                            )
        key: str = method(*args, **kwargs)
        self._redis.rpush("{}:outputs".format(method.__qualname__), key)
        return key

    return wrapper


class Cache:
    """Cache Class

    """

    def __init__(self) -> None:
        """Initialize the Cache instance.

        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def get(self, key: str, fn: typing.Callable = None) -> typing.Union[
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


def replay(method: typing.Callable) -> None:
    """Displays the history of calls to a method

    Args:
        method (typing.Callable): Method to check history.
    """
    key_head = method.__qualname__
    redis_s = redis.Redis()
    inputs = redis_s.lrange("{}:inputs".format(method.__qualname__), 0, -1)
    outputs = redis_s.lrange("{}:outputs".format(method.__qualname__), 0, -1)
    data = zip(inputs, outputs)

    print("{} was called {} times:".format(key_head, len(inputs)))
    for inp, out in data:
        print("{}(*{}) -> {}".format(
                                        key_head,
                                        inp.decode("utf-8"),
                                        out.decode("utf-8")))
