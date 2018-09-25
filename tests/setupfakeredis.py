from unittest import TestCase
import fakeredis
from controllers import brewerylist
from models import cloudredis


class TestwithFakeRedis(TestCase):

    def setUp(self):
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)
        assert cloudredis.REDIS_SERVER == fake

    def tearDown(self):
        cloudredis.REDIS_SERVER.flushall()
        cloudredis.REDIS_SERVER = None