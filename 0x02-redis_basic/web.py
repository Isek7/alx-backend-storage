#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis

r = redis.Redis()

def cache(func):
    def wrapper(url):
        key = f"result:{url}"
        count_key = f"count:{url}"
        result = r.get(key)
        if result is not None:
            r.incr(count_key)
            return result.decode('utf-8')
        else:
            result = func(url)
            r.setex(key, 10, result)
            r.set(count_key, 1)
            return result
    return wrapper

@cache
def get_page(url):
    response = requests.get(url)
    return response.text
