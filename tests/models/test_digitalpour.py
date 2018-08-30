from unittest import TestCase
from models.digitalpour import DigitalPourPage
from models.digitalpour import brewery_info


class TestDigitalPourpage(TestCase):
    def test_DigitalPour_read(self):
        for brewery in brewery_info:
            ut = DigitalPourPage(brewery=brewery)
            assert ut is not None
            ut = None

    def test_DigitalPour_beerlist(self):
        for brewery in brewery_info:
            ut = DigitalPourPage(brewery=brewery)
            assert ut is not None
            beer_string = ut.alexa_taplist()
            assert beer_string is not None
