from unittest import TestCase
from models.breweries.beermenus import BeerMenusPage
from models.breweries.beermenus import brewery_info


class TestBeerMenuspage(TestCase):
    def test_BeerMenus_read(self):
        for brewery in brewery_info:
            ut = BeerMenusPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_BeerMenus_beerlist(self):
        ut = BeerMenusPage(mocked=True)
        assert ut is not None
        for brewery in brewery_info:
            ut.fetch_taplist(brewery=brewery)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn = '../beerlister/tests/data/' + brewery.replace(' ', '') + '.SSML'
            fp = open(fn, mode='r', encoding='utf8')
            tst_data = fp.read()
            fp.close()
            assert (tst_data == beer_string)  # anything different, raise hell!
