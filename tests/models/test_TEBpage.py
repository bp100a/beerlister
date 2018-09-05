from unittest import TestCase
from models.breweries.TEB import TEBpage
import os

class TestTEBpage(TestCase):

    def data_dir(self) -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def test_TEB_read(self):
        teb = TEBpage(mocked=True)
        assert (teb is not None)

    def test_TEB_beerlist(self):
        teb = TEBpage(mocked=True)
        assert teb is not None
        teb.fetch_taplist(brewery="Twin Elephant")
        beer_string = teb.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        fn = self.data_dir() + teb._brewery_name.replace(' ', '') + '.SSML'
        fp = open(fn, mode='r', encoding='utf8')
        tst_data = fp.read()
        fp.close()
        assert (tst_data == beer_string)  # anything different, raise hell!

    def test_TEB_aliases(self):
        teb = TEBpage(mocked=True)
        assert teb is not None

        # see if aliases exist
        found = teb.brewery_by_alias("TEB")
        assert(found == "Twin Elephant")

        found = teb.brewery_by_alias("Twin Elephant Brewing")
        assert(found == "Twin Elephant")

        found = teb.brewery_by_alias("Twin Elephant")
        assert(found == "Twin Elephant")

    def test_TEB_shortname(self):
        teb = TEBpage()
        names = teb.short_name()
        assert(len(names) == 1)
        assert(names[0] == 'Twin Elephant')
