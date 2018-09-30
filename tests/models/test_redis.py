import time
import os
from tests.setupfakeredis import TestwithFakeRedis
from models import cloudredis
import fakeredis


class TestRedis(TestwithFakeRedis):
    """test our redis server setup & connection"""
    def set_environment_variables(self):
        os.environ['REDIS_HOST'] = "MY_REDIS_SERVER"
        os.environ['REDIS_PASSWORD'] = "MY_REDIS_PASSWORD"
        os.environ['REDIS_PORT'] = "12345"

    def test_redis_setup(self):
        self.set_environment_variables()
        redis_host, redis_password, redis_port = cloudredis.read_configuration()
        assert redis_host is not None and redis_password is not None and redis_port is not None
        assert redis_port.isdigit()

    def test_fail_read_configuration(self):
        self.set_environment_variables()
        redis_server, redis_password, redis_port = cloudredis.read_configuration()
        del os.environ['REDIS_HOST']
        redis_host, redis_password, redis_port = cloudredis.read_configuration()
        assert redis_host is None and redis_password is None and redis_port is None

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
