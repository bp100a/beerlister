"""Test cases for pages hosted by UnTappd"""

from unittest import TestCase
from models.breweries.untappd import UnTappdPage
from models.breweries.untappd import BREWERY_INFO
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking
from models import cloudredis


class TestUntappdpage(TestwithMocking):
    """test for pages hosted by UnTappd"""

    # def test_live_pinelands_read(self):
    #     """Test we can access all breweries we know about"""
    #     untapped_page = UnTappdPage(brewery='Pinelands', mocked=False)
    #     untapped_page.fetch_taplist(brewery='Pinelands')
    #     ssml_beer_list = untapped_page.ssml_taplist()
    #     assert ssml_beer_list

    def test_Untappd_read(self):
        """Test we can access all breweries we know about"""
        for brewery in BREWERY_INFO:
            untapped_page = UnTappdPage(brewery=brewery, mocked=True)
            assert untapped_page is not None
            untapped_page = None

    def test_UnTappd_mocked_brewery(self):
        """Test that we cna read brewery pages and validate results"""
        untapped_page = UnTappdPage(mocked=True)
        for brewery_name in BREWERY_INFO:
            # we are mocking the URL, reading a local test file (../tests/data/<brewery>.HTML)
            assert untapped_page is not None
            untapped_page.fetch_taplist(brewery=brewery_name)
            beer_string = untapped_page.ssml_taplist()
            assert beer_string is not None
            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            file_name = data_dir() + brewery_name.replace(" ", "") + ".SSML"
            file_pointer = open(file_name, "r", encoding="utf-8")
            tst_data = file_pointer.read()
            file_pointer.close()
            if tst_data != beer_string:
                assert tst_data == beer_string  # anything different, raise hell!

    def test_untied_brewing_mocked(self):
        """Special testing for Untied Brewing since it does special parsing"""
        brewery_name = "Untied"
        untapped_page = UnTappdPage(mocked=True)
        untapped_page.fetch_taplist(brewery=brewery_name)
        beer_string = untapped_page.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + brewery_name.replace(" ", "") + ".SSML"
        file_pointer = open(file_name, "r", encoding="utf-8")
        tst_data = file_pointer.read()
        file_pointer.close()
        if tst_data != beer_string:
            assert tst_data == beer_string  # anything different, raise hell!

    def test_UnTapped_mocked_brewery_in_cache(self):

        # ensure we start with an empty cache
        brewery_name = next(iter(BREWERY_INFO))
        cloudredis.flush_cache(brewery_name)

        # fetch our brewery information
        untapped_page = UnTappdPage(mocked=True)
        untapped_page.fetch_taplist(brewery=brewery_name)
        uncached_html = untapped_page.ssml_taplist()

        # now let's get it from the cache
        untapped_page = UnTappdPage(mocked=True)
        untapped_page.fetch_taplist(brewery=brewery_name)
        cached_html = untapped_page.ssml_taplist()

        assert cached_html == uncached_html

        # now check the value returned
        file_name = data_dir() + brewery_name.replace(" ", "") + ".HTML"
        file_pointer = open(file_name, mode="r", encoding="utf8")
        brewery_html = file_pointer.read()
        file_pointer.close()
        assert cloudredis.is_cached(brewery_name, brewery_html)

    def test_UnTappd_aliases(self):
        """Test to validate all aliases"""
        untapped_page = UnTappdPage(mocked=True)
        assert untapped_page is not None

        # see if aliases exist
        found = untapped_page.brewery_by_alias("TEB")
        assert found is None

        found = untapped_page.brewery_by_alias("Alementary")
        assert found == "Alementary"

        found = untapped_page.brewery_by_alias("Alementary Brewery")
        assert found == "Alementary"

        # found = untapped_page.brewery_by_alias("Angry Erik Brewing")
        # assert found == "Angry Erik"

        found = untapped_page.brewery_by_alias("Man Skirt")
        assert found == "Man Skirt"

        found = untapped_page.brewery_by_alias("Man Skirt Brewery")
        assert found == "Man Skirt"

    def test_shortnames(self):
        """Test we have the proper short names"""
        untapped_page = UnTappdPage()
        short_names = untapped_page.short_name()
        assert "Man Skirt" in short_names
        # assert 'Angry Erik' in short_names
        assert "Alementary" in short_names
