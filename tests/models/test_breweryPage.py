from unittest import TestCase
import requests
import requests_mock
from models.breweries.beerlist import BreweryPage


class TestBreweryPage(TestCase):

    def test_read(self):
        """Test we can read a brewery page from our base class"""
        mock_url = 'mock://brewery.com'
        bp = BreweryPage(url=mock_url)
        s = requests.Session()
        adapter = requests_mock.Adapter()
        s.mount('mock', adapter)
        adapter.register_uri('GET', mock_url, text='<html><body><div class="field-item"> <div class="beer-holder"></div></div></body></html>')
        assert bp.read_page(in_session=s) is True
