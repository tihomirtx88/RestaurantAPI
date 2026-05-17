import time

cache_store = {}

def set_cache(key, data, ttl=60):
    cache_store[key] = {
        "data": data,
        "expires": time.time() + ttl
    }

def get_cache(key):

    item = cache_store.get(key)

    if not item:
        return None

    if item["expires"] < time.time():
        del cache_store[key]
        return None

    return item["data"]