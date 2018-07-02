from unittest import TestCase
from models.TEB import TEBpage


class TestTEBpage(TestCase):
    def test_TEB_read(self):
        teb = TEBpage()
        assert (teb is not None)

    def test_TEB_beerlist(self):
        teb = TEBpage()
        assert teb is not None

        beer_string = teb.alexa_taplist()
        assert beer_string is not None
