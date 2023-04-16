#!/usr/bin/env python3
"""Implement a get_page

"""
import redis
import requests
import functools
import typing


redie = redis.Redis()
count = 0


def cache(function: typing.Callable) -> typing.Callable:
    """Caches the time a url is accessed

    Args:
        function: request function to cache.

    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        url = args[0]
        redie.set("cached:{}".format(url))
        response = function(*args, **kwargs)
        redie.incr("count:{}".format(url))
        redie.setex("cached:{}".format(url), 10, redie.get("cached:{}".format(url)))
        return response

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
