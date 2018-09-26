from unittest import TestCase
import os
from models.breweries.twinelephant import TEBpage
from tests.models.common import data_dir
from tests.setupfakeredis import TestwithFakeRedis


class TestTEBpage(TestwithFakeRedis):

    def live_TEB_read(self):
        teb = TEBpage(mocked=False)
        assert teb is not None
        teb.fetch_taplist(brewery="Twin Elephant")

    def test_TEB_read(self):
        """Test simple instantiation of TEB page"""
        teb = TEBpage(mocked=True)
        assert teb is not None

    def test_TEB_beerlist(self):
        """Test we can read the Twin Elephant beer list!"""
        teb = TEBpage(mocked=True)
        assert teb is not None
        teb.fetch_taplist(brewery="Twin Elephant")
        beer_string = teb.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + teb._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, mode='r', encoding='utf8')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == beer_string  # anything different, raise hell!

    def test_TEB_aliases(self):
        """Test to validate all aliases for brewery"""
        teb = TEBpage(mocked=True)
        assert teb is not None

        # see if aliases exist
        found = teb.brewery_by_alias("TEB")
        assert found == "Twin Elephant"

        found = teb.brewery_by_alias("Twin Elephant Brewing")
        assert found == "Twin Elephant"

        found = teb.brewery_by_alias("Twin Elephant")
        assert found == "Twin Elephant"

    def test_TEB_shortname(self):
        """Test to return proper short name for brewery"""
        teb = TEBpage()
        names = teb.short_name()
        assert len(names) == 1
        assert names[0] == 'Twin Elephant'
