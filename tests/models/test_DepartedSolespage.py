from unittest import TestCase
from models.DepartedSoles import DepartedSolespage


class TestDepartedSolespage(TestCase):
    def test_DepartedSoles_read(self):
        dsp = DepartedSolespage()
        assert (dsp is not None)

    def test_DepartedSoles_beerlist(self):
        dsp = DepartedSolespage()
        assert dsp is not None

        beer_string = dsp.alexa_taplist()
        assert beer_string is not None
