from unittest import TestCase
import os
from models.breweries.departedsoles import DepartedSolespage
from tests.models.common import data_dir


class TestDepartedSolespage(TestCase):
    """test for the departed soles web scraping page"""

    def test_DepartedSoles_read(self):
        """Test that we can do basic read of page"""
        dsp = DepartedSolespage(mocked=True)
        assert dsp is not None

    def test_DepartedSoles_beerlist(self):
        """Test we can get back a properly parsed beer list"""
        dsp = DepartedSolespage(mocked=True)
        assert dsp is not None

        dsp.fetch_taplist(brewery='Departed Soles')
        beer_string = dsp.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + dsp._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, 'r')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == beer_string  # anything different, raise hell!

    def test_DepartedSoles_aliases(self):
        """Test that we cover all alias for this brewery"""
        ds = DepartedSolespage(mocked=True)
        assert ds is not None

        # see if aliases exist
        found = ds.brewery_by_alias("TEB")
        assert found is None

        found = ds.brewery_by_alias("Departed Soles")
        assert found == "Departed Soles"

        found = ds.brewery_by_alias("Departed Soles Brewing")
        assert found == "Departed Soles"

        found = ds.brewery_by_alias("Departed Soles Brewery")
        assert found == "Departed Soles"

    def test_shortnames(self):
        """Test we get the correct short name for this brewery"""
        dp = DepartedSolespage()
        short_names = dp.short_name()
        assert 'Departed Soles' in short_names
        assert len(short_names) == 1
