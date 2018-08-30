from unittest import TestCase
from models.beermenus import BeerMenusPage
from models.beermenus import brewery_info


class TestBeerMenuspage(TestCase):
    def test_BeerMenus_read(self):
        for brewery in brewery_info:
            ut = BeerMenusPage(brewery=brewery)
            assert ut is not None
            ut = None

    def test_BeerMenus_beerlist(self):
        for brewery in brewery_info:
            ut = BeerMenusPage(brewery=brewery)
            assert ut is not None
            beer_string = ut.alexa_taplist()
            assert beer_string is not None
