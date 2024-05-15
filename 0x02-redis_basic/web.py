#!/usr/bin/env python3
'''Task 5: Implementing an expiring web cache and tracker'''
import redis
import requests
from functools import wraps
from typing import Callable


r_store = redis.Redis()


def database(func: Callable) -> Callable:
    '''Caches url content'''
    @wraps(func)
    def wrapper(url) -> str:
        count = f'count:{url}'
        r_store.incr(count)
        result = r_store.get(url)
        if result:
            return result.decode("utf-8")
        result = func(url)
        r_store.set(count, 0)
        r_store.setex(url, 10, result)
        return result
    return wrapper


@database
def get_page(url: str) -> str:
    '''
    It uses the requests module to obtain
    the HTML content of a particular URL and returns it.
    '''
    result = requests.get(url)
    body = result.text
    return body
