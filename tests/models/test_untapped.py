from unittest import TestCase
from models.breweries.untappd import UnTappdPage
from models.breweries.untappd import brewery_info


class TestUntappdpage(TestCase):

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
            fn = '../beerlister/tests/data/' + brewery_name.replace(' ', '') + '.SSML'
            fp = open(fn, 'r')
            tst_data = fp.read()
            fp.close()
            assert(tst_data == beer_string) # anything different, raise hell!

