import time
import os
from tests.setupmocking import TestwithMocking
from models import cloudredis
import fakeredis


class TestRedis(TestwithMocking):
    """test our redis server setup & connection"""

    def test_redis_setup(self):
        redis_host, redis_password, redis_port = cloudredis.read_configuration()
        assert redis_host == 'bogus.redis.endpoint'
        assert redis_password == 'bogus.redis.password'
        assert redis_port == 14405

    def test_redis_initialize(self):
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)
        assert cloudredis.REDIS_SERVER == fake

    def test_cache_ssml(self):
        """test that we can cache our SSML"""
        ssml_to_cache = "ssml to cache"
        html_we_scraped = "html we scraped"
        current_time_as_int = int(time.time())
        brewery_name = "bogus brewing"
        cloudredis.cache_ssml(brewery=brewery_name, html=html_we_scraped, ssml=ssml_to_cache, cached_time=current_time_as_int)

        assert cloudredis.exists(cloudredis.md5_key(brewery_name))
        assert cloudredis.exists(cloudredis.ssml_key(brewery_name))
        assert cloudredis.exists(cloudredis.timestamp_key(brewery_name))

        assert not cloudredis.exists(cloudredis.md5_key("not " + brewery_name))
        assert not cloudredis.exists(cloudredis.ssml_key("not " + brewery_name))
        assert not cloudredis.exists(cloudredis.timestamp_key("not " + brewery_name))

    def test_cache_expiration(self):
        ssml_to_cache = "ssml that will expire"
        html_we_scraped = "html that will expire"
        CACHE_TIMEOUT = 1
        past_time_as_int = int(time.time()) - (CACHE_TIMEOUT*60*60+10)  # 1 hour in past (and a little more for skew)
        brewery_name = "expiring brewery"
        cloudredis.cache_ssml(brewery=brewery_name, html=html_we_scraped, ssml=ssml_to_cache, cached_time=past_time_as_int)

        assert cloudredis.is_cached(brewery_name, html_we_scraped)

        # okay it's cached, now let's expire it
        cloudredis.expired(brewery_name, CACHE_TIMEOUT)

        assert not cloudredis.is_cached(brewery_name, html_we_scraped)

    def test_empty_cache(self):
        assert cloudredis.expired(brewery="not cached", too_many_hours=1)

    def test_value_error(self):
        """force a bad timestamp value to test value error exception"""
        ssml_to_cache = "ssml that will expire"
        html_we_scraped = "html that will expire"
        CACHE_TIMEOUT = 1
        past_time_as_int = int(time.time()) - (CACHE_TIMEOUT*60*60+10)  # 1 hour in past (and a little more for skew)
        brewery_name = "expiring brewery"
        cloudredis.cache_ssml(brewery=brewery_name, html=html_we_scraped, ssml=ssml_to_cache, cached_time=past_time_as_int)

        # now overwrite the timestamp entry
        cloudredis.REDIS_SERVER.set(cloudredis.timestamp_key(brewery_name), float(past_time_as_int))

        # now check it
        assert not cloudredis.is_cached(brewery_name, html_we_scraped)

    def test_md5_not_exist(self):
        """test a cache miss by testing new HTML"""
        ssml_to_cache = "ssml that will expire"
        html_we_scraped = "old html"
        CACHE_TIMEOUT = 1
        past_time_as_int = int(time.time()) - (CACHE_TIMEOUT*60*60+10)  # 1 hour in past (and a little more for skew)
        brewery_name = "changing brewery"
        cloudredis.cache_ssml(brewery=brewery_name, html=html_we_scraped, ssml=ssml_to_cache, cached_time=past_time_as_int)

        assert not cloudredis.md5_exists(brewery=brewery_name, html="new html")
