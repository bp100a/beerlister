from unittest import TestCase
import os
from models.breweries.digitalpour import DigitalPourPage
from models.breweries.digitalpour import BREWERY_INFO
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class TestDigitalPourpage(TestwithMocking):

    def test_DigitalPour_read(self):
        """Test we can read all breweries for this provider"""
        for brewery in BREWERY_INFO:
            ut = DigitalPourPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_DigitalPour_beerlist(self):
        """Test & validate beer list for this provider"""
        ut = DigitalPourPage(mocked=True)
        assert ut is not None
        for brewery in BREWERY_INFO:
            ut.fetch_taplist(brewery=brewery)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            file_name = data_dir() + brewery.replace(' ', '') + '.SSML'
            file_pointer = open(file_name, 'r')
            tst_data = file_pointer.read()
            file_pointer.close()
            assert tst_data == beer_string  # anything different, raise hell!

    def test_DigitalPour_cached(self):
        """Test we can read the Digital Pour beer list!"""
        pour_page = DigitalPourPage(mocked=True)
        assert pour_page is not None
        brewery_name = next(iter(BREWERY_INFO))
        from_cache = pour_page.fetch_taplist(brewery=brewery_name)
        assert not from_cache

        # 2nd read from cache!
        pour_page.ssml_taplist() # this puts it in the cache
        from_cache = pour_page.fetch_taplist(brewery=brewery_name)
        assert from_cache

    def test_DigitalPour_aliases(self):
        """Test we get proper aliases for this brewery"""
        dp = DigitalPourPage(mocked=True)
        assert dp is not None

        # see if aliases exist
        found = dp.brewery_by_alias("TEB")
        assert found is None

        found = dp.brewery_by_alias("Village Idiot")
        assert found == "Village Idiot"

        found = dp.brewery_by_alias("Village Idiot Brewing")
        assert found == "Village Idiot"

        found = dp.brewery_by_alias("Village Idiot Brewery")
        assert found == "Village Idiot"

    def test_shortnames(self):
        """Test we get proper short name for this brewery"""
        dp = DigitalPourPage()
        short_names = dp.short_name()
        assert 'Village Idiot' in short_names
        assert len(short_names) == 1