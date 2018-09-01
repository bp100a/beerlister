from unittest import TestCase
from models.breweries.digitalpour import DigitalPourPage
from models.breweries.digitalpour import brewery_info


class TestDigitalPourpage(TestCase):
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
            fn = '../beerlister/tests/data/' + brewery.replace(' ', '') + '.SSML'
            fp = open(fn, 'r')
            tst_data = fp.read()
            fp.close()
            assert (tst_data == beer_string)  # anything different, raise hell!
