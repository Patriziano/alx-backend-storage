#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:)."""

from redis import Redis
from functools import wraps
from typing import Callable
import requests

db = Redis()


def cache_count(method: Callable) -> Callable:
    """cache count"""
    @wraps(method)
    def wrapper(url):
        """ wrapper for the function """
        key = f'count:{url}'
        db.incr(key)
        if db.get(f'result:{url}'):
            return db.get(f'result:{url}').decode('utf-8')
        result = method(url)
        db.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_count
def get_page(url: str) -> str:
    """get_page function"""
    response = requests.get(url)
    return response.text
