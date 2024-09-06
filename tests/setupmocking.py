"""This is a base class for our Unit Tests that will ensure we
properly setup our mocked outputs such as Redis and logging
"""
from unittest import TestCase
import fakeredis
from models import cloudredis, setuplogging


class TestwithMocking(TestCase):

    def setUp(self):
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)
        assert cloudredis.REDIS_SERVER == fake
        setuplogging.initialize_logging(True)

    def tearDown(self):
        cloudredis.REDIS_SERVER.flushall()
        cloudredis.REDIS_SERVER = None
