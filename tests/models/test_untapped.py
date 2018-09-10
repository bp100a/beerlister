from unittest import TestCase
import os
from models.breweries.untappd import UnTappdPage
from models.breweries.untappd import BREWERY_INFO
from tests.models.common import data_dir


class TestUntappdpage(TestCase):

    def test_Untappd_read(self):
        """Test we can access all breweries we know about"""
        for brewery in BREWERY_INFO:
            ut = UnTappdPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_UnTappd_mocked_brewery(self):
        """Test that we cna read brewery pages and validate results"""
        ut = UnTappdPage(mocked=True)
        for brewery_name in BREWERY_INFO:
            # we are mocking the URL, reading a local test file (../tests/data/<brewery>.HTML)
            assert ut is not None
            ut.fetch_taplist(brewery=brewery_name)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None
            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            file_name = data_dir() + brewery_name.replace(' ', '') + '.SSML'
            file_pointer = open(file_name, 'r')
            tst_data = file_pointer.read()
            file_pointer.close()
            if tst_data != beer_string:
                assert tst_data == beer_string # anything different, raise hell!

    def test_UnTappd_aliases(self):
        """Test to validate all aliases"""
        ut = UnTappdPage(mocked=True)
        assert ut is not None

        # see if aliases exist
        found = ut.brewery_by_alias("TEB")
        assert found is None

        found = ut.brewery_by_alias("Alementary")
        assert found == "Alementary Brewing"

        found = ut.brewery_by_alias("Alementary Brewery")
        assert found == "Alementary Brewing"

        found = ut.brewery_by_alias("Angry Erik Brewing")
        assert found == "Angry Erik"

        found = ut.brewery_by_alias("Man Skirt")
        assert found == "Man Skirt Brewing"

        found = ut.brewery_by_alias("Man Skirt Brewery")
        assert found == "Man Skirt Brewing"

        found = ut.brewery_by_alias("Demented")
        assert found == "Demented Brewing"

        found = ut.brewery_by_alias("Demented Brewery")
        assert found == "Demented Brewing"

    def test_shortnames(self):
        """Test we have the proper short names"""
        ut = UnTappdPage()
        short_names = ut.short_name()
        assert 'Man Skirt' in short_names
        assert 'Demented' in short_names
        assert 'Angry Erik' in short_names
        assert 'Alementary' in short_names