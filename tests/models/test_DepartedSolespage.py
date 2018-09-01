from unittest import TestCase
from models.breweries.DepartedSoles import DepartedSolespage


class TestDepartedSolespage(TestCase):
    def test_DepartedSoles_read(self):
        dsp = DepartedSolespage(mocked=True)
        assert (dsp is not None)

    def test_DepartedSoles_beerlist(self):
        dsp = DepartedSolespage(mocked=True)
        assert dsp is not None

        dsp.fetch_taplist()
        beer_string = dsp.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        fn = '../beerlister/tests/data/' + dsp._brewery_name.replace(' ', '') + '.SSML'
        fp = open(fn, 'r')
        tst_data = fp.read()
        fp.close()
        assert (tst_data == beer_string)  # anything different, raise hell!
