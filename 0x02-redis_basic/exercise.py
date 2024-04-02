#!/usr/bin/env python3
"""To create a cache class in redis"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def replay(method: Callable):
    """ replay function to display function history """
    cache = redis.Redis()
    name = method.__qualname__
    kinput = name + ':inputs'
    koutput = name + ':outputs'
    i_list = cache.lrange(kinput, 0, -1)
    o_list = cache.lrange(koutput, 0, -1)
    c_list = list(zip(i_list, o_list))
    print(f'{name} was called {len(c_list)} times:')
    for key, value in c_list:
        print(f"{name}(*{key.decode('utf-8')}) -> \
{value.decode('utf-8')}")


def count_calls(method: Callable) -> Callable:
    """count function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """call history"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        kinputs = method.__qualname__ + ":inputs"
        koutputs = method.__qualname__ + ":outputs"
        self._redis.rpush(kinputs, str(args))
        value = method(self, *args, **kwargs)
        self._redis.rpush(koutputs, str(value))
        return value
    return wrapper


class Cache:
    """cache class"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None) \
            -> Union[str, bytes, int, None]:
        """the get"""
        value = self._redis.get(key)

        if value is not None and fn is not None:
            value = fn(value)

        return value

    def get_str(self, key: str) -> Union[str, None]:
        """get_str method"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=lambda x: int(x) if x else None)
