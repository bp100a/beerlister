from unittest import TestCase
from models.breweries.DepartedSoles import DepartedSolespage
import os

class TestDepartedSolespage(TestCase):

    def data_dir(self) -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def test_DepartedSoles_read(self):
        dsp = DepartedSolespage(mocked=True)
        assert (dsp is not None)

    def test_DepartedSoles_beerlist(self):
        dsp = DepartedSolespage(mocked=True)
        assert dsp is not None

        dsp.fetch_taplist(brewery='Departed Soles')
        beer_string = dsp.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        fn =  self.data_dir() + dsp._brewery_name.replace(' ', '') + '.SSML'
        fp = open(fn, 'r')
        tst_data = fp.read()
        fp.close()
        assert (tst_data == beer_string)  # anything different, raise hell!

    def test_DepartedSoles_aliases(self):
        ds = DepartedSolespage(mocked=True)
        assert ds is not None

        # see if aliases exist
        found = ds.brewery_by_alias("TEB")
        assert(found is None)

        found = ds.brewery_by_alias("Departed Soles")
        assert(found == "Departed Soles")

        found = ds.brewery_by_alias("Departed Soles Brewing")
        assert(found == "Departed Soles")

        found = ds.brewery_by_alias("Departed Soles Brewery")
        assert(found == "Departed Soles")

    def test_shortnames(self):
        dp = DepartedSolespage()
        short_names = dp.short_name()
        assert ('Departed Soles' in short_names)
        assert(len(short_names) == 1)
