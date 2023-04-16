#!/usr/bin/env python3
"""Implement a get_page

"""
import redis
import requests
import functools
import typing


redie = redis.Redis()


def cache(function: typing.Callable) -> typing.Callable:
    """Caches the time a url is accessed

    Args:
        function: request function to cache.

    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        url = args[0]
        with redie.pipeline as pipe:
            pipe.watch("count:{}".format(url))
            pipe.multi()
            pipe.incr("count:{}".format(url))
            pipe.expire("count:{}".format(url), 10)
            pipe.execute()
        return function(*args, **kwargs)

    return wrapper


@cache
def get_page(url: str) -> str:
    """Gets an returns a url page

    Args:
        url (str): String link.

    Returns:
        Request object.
    """
    page = requests.get(url)
    return page
