from unittest import TestCase
from models.untappd import UnTappdPage
from models.untappd import brewery_info


class TestUntappdpage(TestCase):

    def test_Untappd_read(self):
        for brewery in brewery_info:
            ut = UnTappdPage(brewery=brewery)
            assert ut is not None
            ut = None

    def test_UnTappd_mocked_brewery(self):
        for brewery_name in brewery_info:
            # we are mocking the URL, reading a local test file (../tests/data/<brewery>.HTML)
            ut = UnTappdPage(brewery=brewery_name, mocked=True)
            assert ut is not None
            beer_string = ut.alexa_taplist()
            assert beer_string is not None
            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn = '../data/' + brewery_name.replace(' ', '') + '.SSML'
            fp = open(fn, 'r')
            tst_data = fp.read()
            assert(tst_data == beer_string) # anything different, raise hell!

