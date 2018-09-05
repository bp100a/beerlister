from unittest import TestCase
from models.breweries.untappd import UnTappdPage
from models.breweries.untappd import brewery_info
import os

class TestUntappdpage(TestCase):

    def data_dir(self) -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def test_Untappd_read(self):
        for brewery in brewery_info:
            ut = UnTappdPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_UnTappd_mocked_brewery(self):
        ut = UnTappdPage(mocked=True)
        for brewery_name in brewery_info:
            # we are mocking the URL, reading a local test file (../tests/data/<brewery>.HTML)
            assert ut is not None
            ut.fetch_taplist(brewery=brewery_name)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None
            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn = self.data_dir() + brewery_name.replace(' ', '') + '.SSML'
            fp = open(fn, 'r')
            tst_data = fp.read()
            fp.close()
            assert(tst_data == beer_string) # anything different, raise hell!

    def test_UnTappd_aliases(self):
        ut = UnTappdPage(mocked=True)
        assert ut is not None

        # see if aliases exist
        found = ut.brewery_by_alias("TEB")
        assert(found is None)

        found = ut.brewery_by_alias("Alementary")
        assert(found == "Alementary Brewing")

        found = ut.brewery_by_alias("Alementary Brewery")
        assert(found == "Alementary Brewing")

        found = ut.brewery_by_alias("Angry Erik Brewing")
        assert(found == "Angry Erik")

        found = ut.brewery_by_alias("Man Skirt")
        assert(found == "Man Skirt Brewing")

        found = ut.brewery_by_alias("Man Skirt Brewery")
        assert(found == "Man Skirt Brewing")

        found = ut.brewery_by_alias("Demented")
        assert(found == "Demented Brewing")

        found = ut.brewery_by_alias("Demented Brewery")
        assert(found == "Demented Brewing")
