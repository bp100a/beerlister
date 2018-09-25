"""Test cases for pages hosted by UnTappd"""
from unittest import TestCase
from models.breweries.untappd import UnTappdPage
from models.breweries.untappd import BREWERY_INFO
from tests.models.common import data_dir
from tests.setupfakeredis import TestwithFakeRedis
from models import cloudredis


class TestUntappdpage(TestwithFakeRedis):
    """test for pages hosted by UnTappd"""

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
            file_name = data_dir() + brewery_name.replace(' ', '') + '.SSML'
            file_pointer = open(file_name, 'r')
            tst_data = file_pointer.read()
            file_pointer.close()
            if tst_data != beer_string:
                assert tst_data == beer_string # anything different, raise hell!

    def test_UnTapped_mocked_brewery_in_cache(self):

        # ensure we start with an empty cache
        for brewery_name in BREWERY_INFO:
            cloudredis.flush_cache(brewery_name)

        # first call to fill the cache
        self.test_UnTappd_mocked_brewery()

        # now read breweries from cache
        self.test_UnTappd_mocked_brewery()

        # now just run through the cache for each brewery and validate
        for brewery_name in BREWERY_INFO:
            file_name = data_dir() + brewery_name.replace(' ', '') + '.HTML'
            file_pointer = open(file_name, mode='r', encoding='utf8')
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

        found = untapped_page.brewery_by_alias("Angry Erik Brewing")
        assert found == "Angry Erik"

        found = untapped_page.brewery_by_alias("Man Skirt")
        assert found == "Man Skirt"

        found = untapped_page.brewery_by_alias("Man Skirt Brewery")
        assert found == "Man Skirt"

        found = untapped_page.brewery_by_alias("Demented")
        assert found == "Demented"

        found = untapped_page.brewery_by_alias("Demented Brewery")
        assert found == "Demented"

    def test_shortnames(self):
        """Test we have the proper short names"""
        untapped_page = UnTappdPage()
        short_names = untapped_page.short_name()
        assert 'Man Skirt' in short_names
        assert 'Demented' in short_names
        assert 'Angry Erik' in short_names
        assert 'Alementary' in short_names
