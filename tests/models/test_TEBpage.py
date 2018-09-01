from unittest import TestCase
from models.breweries.TEB import TEBpage


class TestTEBpage(TestCase):
    def test_TEB_read(self):
        teb = TEBpage(mocked=True)
        assert (teb is not None)

    def test_TEB_beerlist(self):
        teb = TEBpage(mocked=True)
        assert teb is not None
        teb.fetch_taplist()
        beer_string = teb.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        fn = '../beerlister/tests/data/' + teb._brewery_name.replace(' ', '') + '.SSML'
        fp = open(fn, mode='r', encoding='utf8')
        tst_data = fp.read()
        fp.close()
        assert (tst_data == beer_string)  # anything different, raise hell!
