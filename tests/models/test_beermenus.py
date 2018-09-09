from unittest import TestCase
from models.breweries.beermenus import BeerMenusPage
from models.breweries.beermenus import BREWERY_INFO
import os

class TestBeerMenuspage(TestCase):

    def data_dir(self) -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def test_BeerMenus_read(self):
        for brewery in BREWERY_INFO:
            ut = BeerMenusPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_BeerMenus_beerlist(self):
        ut = BeerMenusPage(mocked=True)
        assert ut is not None
        for brewery in BREWERY_INFO:
            ut.fetch_taplist(brewery=brewery)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn = self.data_dir() + brewery.replace(' ', '') + '.SSML'
            fp = open(fn, mode='r', encoding='utf8')
            tst_data = fp.read()
            fp.close()
            assert (tst_data == beer_string)  # anything different, raise hell!

    def test_BeerMenus_aliases(self):
        bp = BeerMenusPage(mocked=True)
        assert bp is not None
        # see if aliases exist
        found = bp.brewery_by_alias("TEB")
        assert(found is None)

        found = bp.brewery_by_alias("Rinn Duin")
        assert(found == "Rinn Duin Brewing")

        found = bp.brewery_by_alias("Rinn Duin Brewing")
        assert(found == "Rinn Duin Brewing")

        found = bp.brewery_by_alias("Rinn Duin Brewery")
        assert(found == "Rinn Duin Brewing")

    def test_shortnames(self):
        bp = BeerMenusPage()
        short_names = bp.short_name()
        assert ('Rinn Duin' in short_names)
        assert(len(short_names) == 1)