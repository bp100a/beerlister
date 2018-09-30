"""here's where we manage our redis cache"""
import os
import time
import hashlib
import redis


REDIS_SERVER = None
CACHE_TIMEOUT = 2

def read_configuration():
    """read the redis server configuration from the
    environment variables"""
    try:
        redis_endpoint = os.environ['REDIS_HOST']
        redis_password = os.environ['REDIS_PASSWORD']
        redis_port = os.environ['REDIS_PORT']
    except Exception:
        return None, None, None

    return redis_endpoint, redis_password, redis_port


def initialize_cloud_redis(injected_server=None):
    """
    Initialize the redis cloud server. Read environment
    variables to get our endpoint & passphrase:

    REDIS_HOST
    REDIS_PASSWORD
    REDIS_PORT
    :return:
    """
    global REDIS_SERVER
    if injected_server is None:
        if REDIS_SERVER is not None: # if we have a redis instance, return it
            return
        redis_endpoint, redis_password, redis_port = read_configuration()
        redis_server = redis.Redis(host=redis_endpoint,
                                   port=redis_port,
                                   password=redis_password)
    else:
        # injecting a fake redis will always override existing instance
        redis_server = injected_server

    REDIS_SERVER = redis_server
    return


def exists(redis_key: str) -> bool:
    """returns True if the specified key exists in the cache"""
    global REDIS_SERVER
    assert REDIS_SERVER is not None

    return REDIS_SERVER.exists(redis_key) == 1


def md5_key(brewery: str) -> str:
    """create key for the md5 value"""
    return brewery.replace(' ', '') + "_md5"


def ssml_key(brewery: str) -> str:
    """create key for the ssml value"""
    return brewery.replace(' ', '') + "_ssml"


def timestamp_key(brewery: str) -> str:
    """create key for the timestamp value (an integer)"""
    return brewery.replace(' ', '') + "_timestamp"


def flush_cache(brewery: str) -> None:
    """flush the cache entries"""
    global REDIS_SERVER
    REDIS_SERVER.delete(md5_key(brewery))
    REDIS_SERVER.delete(ssml_key(brewery))
    REDIS_SERVER.delete(timestamp_key(brewery))


def md5_exists(brewery: str, html: str) -> bool:
    """given a brewery name and it's HTML page
    compute the MD5 and see if we have a cached entry
    for it"""
    global REDIS_SERVER
    if not exists(md5_key(brewery)):
        return False

    # okay the key exists, make sure it hasn't expired
    if expired(brewery, too_many_hours=CACHE_TIMEOUT):
        return False

    # the value exists and it hasn't expired, so check the
    # hash
    md5 = hashlib.md5()
    md5.update(html.encode('utf-8'))
    current_md5 = md5.digest()
    cached_md5 = REDIS_SERVER.get(md5_key(brewery))
    if cached_md5 == current_md5:
        return True

    # if they don't match then cache no longer valid - FLUSH IT!
    flush_cache(brewery)
    return False


def expired(brewery: str, too_many_hours: int) -> bool:
    """check the timestamp key and see if it has expired
    all timestamps are floats in seconds, so just make them ints"""
    global REDIS_SERVER

    str_timestamp = REDIS_SERVER.get(timestamp_key(brewery))
    if str_timestamp is None:
        return True

    # since all timestamps are floats and in seconds
    # we only need the integer portion
    try:
        cached_timestamp = int(str_timestamp)
    except ValueError:
        flush_cache(brewery)
        return True

    now_timestamp = int(time.time())
    elapsed_seconds = now_timestamp - cached_timestamp
    assert elapsed_seconds >= 0
    elapsed_hours = int(elapsed_seconds / 3600)
    # if the cache has expired, flush it
    if elapsed_hours >= too_many_hours:
        flush_cache(brewery)
        return True

    return False  # cached values still useful


def ssml_from_cache(brewery: str) -> str:
    """
    We should only be calling this when we know the
    cache entry is valid - after we check expiration & md5
    :param brewery:
    :return:
    """

    ssml_output = REDIS_SERVER.get(ssml_key(brewery))
    if isinstance(ssml_output, bytes):
        ssml_output = ssml_output.decode('utf-8')

    return ssml_output


def cache_ssml(brewery: str, html: str, ssml: str, cached_time: int) -> None:
    """

    :param brewery: name of the brewery
    :param html: html scraped from brewery page
    :param ssml: speech output generated from scraped html
    :param cached_time: time we are caching (useful for testing)
    :return:
    """
    assert brewery is not None and ssml is not None and cached_time is not None
    global REDIS_SERVER

    md5 = hashlib.md5()
    md5.update(html.encode('utf-8'))
    md5_response = md5.digest()
    REDIS_SERVER.set(md5_key(brewery), md5_response)
    REDIS_SERVER.set(ssml_key(brewery), ssml)
    REDIS_SERVER.set(timestamp_key(brewery), cached_time)


def is_cached(brewery, rsp_text) -> bool:
    """Check to see if this brewery's webpage has already
    been read and we can save a lot of work
    =True, then we have a cache of this response"""
    assert brewery is not None and rsp_text is not None

    # check if there's a valid cache entry
    return md5_exists(brewery, rsp_text)
