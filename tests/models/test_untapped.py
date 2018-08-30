from unittest import TestCase
from models.untappd import UnTappdPage
from models.untappd import brewery_info


class TestUntappdpage(TestCase):
    def test_Untappd_read(self):
        for brewery in brewery_info:
            ut = UnTappdPage(brewery=brewery)
            assert ut is not None
            ut = None

    def test_UnTappd_beerlist(self):
        for brewery in brewery_info:
            ut = UnTappdPage(brewery=brewery)
            assert ut is not None
            beer_string = ut.alexa_taplist()
            assert beer_string is not None
