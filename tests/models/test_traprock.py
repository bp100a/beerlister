import os
from models.breweries.traprock import TrapRockPage
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class TestTrapRockpage(TestwithMocking):
    """test for the departed soles web scraping page"""

    def test_TrapRockPage_read(self):
        """Test that we can do basic read of page"""
        trap_rock_page = TrapRockPage(mocked=True)
        assert trap_rock_page is not None
        status = trap_rock_page.fetch_taplist(brewery='Trap Rock')
        assert not status

    def test_TrapRockPage_ssml(self):
        trap_rock_page = TrapRockPage(mocked=True)
        assert trap_rock_page is not None
        status = trap_rock_page.fetch_taplist(brewery='Trap Rock')
        assert not status
        ssml = trap_rock_page.ssml_taplist()
        assert ssml
        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + trap_rock_page._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, mode='r', encoding='utf8')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == ssml  # anything different, raise hell!
