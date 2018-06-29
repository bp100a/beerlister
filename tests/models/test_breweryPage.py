from unittest import TestCase
from models.beerlist import BreweryPage
import requests
import requests_mock


class TestBreweryPage(TestCase):
    def test_read(self):
        mock_url = 'mock://brewery.com'
        bp = BreweryPage(url=mock_url)
        s = requests.Session()
        adapter = requests_mock.Adapter()
        s.mount('mock', adapter)
        adapter.register_uri('GET', mock_url, text='<html><body><div class="field-item"> <div class="beer-holder"></div></div></body></html>')
        assert(bp.read(session=s) is True)

    def test_TEBlive_read(self):
        bp = BreweryPage(url="https://twinelephant.com")
        assert(bp.read() is True)