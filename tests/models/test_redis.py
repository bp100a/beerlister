import time
from tests.setupfakeredis import TestwithFakeRedis
from models import cloudredis
import fakeredis


class TestRedis(TestwithFakeRedis):
    """test our redis server setup & connection"""
    def test_redis_setup(self):
        redis_host, redis_password, redis_port = cloudredis.read_configuration()
        assert redis_host is not None and redis_password is not None and redis_port is not None
        assert redis_port.isdigit()

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
        past_time_as_int = int(time.time()) - (1*60*60+10)  # 1 hour in past (and a little more for skew)
        brewery_name = "expiring brewery"
        cloudredis.cache_ssml(brewery=brewery_name, html=html_we_scraped, ssml=ssml_to_cache, cached_time=past_time_as_int)

        assert cloudredis.is_cached(brewery_name, html_we_scraped)

        # okay it's cached, now let's expire it
        cloudredis.expired(brewery_name, 1)

        assert not cloudredis.is_cached(brewery_name, html_we_scraped)