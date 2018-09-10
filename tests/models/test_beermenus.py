from unittest import TestCase
import os
from models.breweries.beermenus import BeerMenusPage
from models.breweries.beermenus import BREWERY_INFO
from tests.models.common import data_dir

class TestBeerMenuspage(TestCase):

    def test_BeerMenus_read(self):
        """Test that we can read beer menu pages for all known breweries"""
        for brewery in BREWERY_INFO:
            ut = BeerMenusPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_BeerMenus_beerlist(self):
        """Test that we get back a properly parsed beer list"""
        ut = BeerMenusPage(mocked=True)
        assert ut is not None
        for brewery in BREWERY_INFO:
            ut.fetch_taplist(brewery=brewery)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn = data_dir() + brewery.replace(' ', '') + '.SSML'
            fp = open(fn, mode='r', encoding='utf8')
            tst_data = fp.read()
            fp.close()
            assert tst_data == beer_string  # anything different, raise hell!

    def test_BeerMenus_aliases_bad(self):
        """Test that a bad beer alias will fail"""
        bp = BeerMenusPage(mocked=True)
        assert bp is not None
        # see if aliases exist
        found = bp.brewery_by_alias("TEB")
        assert found is None

    def test_BeerMenus_aliases_good(self):
        """Test that we can process proper alias for breweries"""
        bp = BeerMenusPage(mocked=True)
        found = bp.brewery_by_alias("Rinn Duin")
        assert found == "Rinn Duin Brewing"

        found = bp.brewery_by_alias("Rinn Duin Brewing")
        assert found == "Rinn Duin Brewing"

        found = bp.brewery_by_alias("Rinn Duin Brewery")
        assert found == "Rinn Duin Brewing"

    def test_shortnames(self):
        """Test that we get back the short name for our brewery"""
        bp = BeerMenusPage()
        short_names = bp.short_name()
        assert 'Rinn Duin' in short_names
        assert len(short_names) == 1
