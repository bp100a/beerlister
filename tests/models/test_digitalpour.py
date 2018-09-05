from unittest import TestCase
from models.breweries.digitalpour import DigitalPourPage
from models.breweries.digitalpour import brewery_info
import os


class TestDigitalPourpage(TestCase):

    @staticmethod
    def data_dir() -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def test_DigitalPour_read(self):
        for brewery in brewery_info:
            ut = DigitalPourPage(brewery=brewery, mocked=True)
            assert ut is not None
            ut = None

    def test_DigitalPour_beerlist(self):
        ut = DigitalPourPage(mocked=True)
        assert ut is not None
        for brewery in brewery_info:
            ut.fetch_taplist(brewery=brewery)
            beer_string = ut.ssml_taplist()
            assert beer_string is not None

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn = self.data_dir() + brewery.replace(' ', '') + '.SSML'
            fp = open(fn, 'r')
            tst_data = fp.read()
            fp.close()
            assert (tst_data == beer_string)  # anything different, raise hell!

    def test_DigitalPour_aliases(self):
        dp = DigitalPourPage(mocked=True)
        assert dp is not None

        # see if aliases exist
        found = dp.brewery_by_alias("TEB")
        assert(found is None)

        found = dp.brewery_by_alias("Village Idiot")
        assert(found == "Village Idiot")

        found = dp.brewery_by_alias("Village Idiot Brewing")
        assert(found == "Village Idiot")

        found = dp.brewery_by_alias("Village Idiot Brewery")
        assert(found == "Village Idiot")

    def test_shortnames(self):
        dp = DigitalPourPage()
        short_names = dp.short_name()
        assert ('Village Idiot' in short_names)
        assert(len(short_names) == 1)