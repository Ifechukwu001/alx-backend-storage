#!/usr/bin/env python3
"""Implement a get_page

"""
import redis
import requests


def get_page(url: str) -> str:

    redie = redis.Redis()
    def wrapper():
        redie.incr("count:{}".format(url))
        redie.expire("count:{}".format(url), 10)

        page = requests.get(url)
        return page.text

    return wrapper()
