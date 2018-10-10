import os
from models.breweries.angryerik import AngryErikPage
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class TestAngryErkipage(TestwithMocking):
    """test for the departed soles web scraping page"""

    def test_AngryErikPage_read(self):
        """Test that we can do basic read of page"""
        angry_erik_page = AngryErikPage(mocked=True)
        assert angry_erik_page is not None
        status = angry_erik_page.fetch_taplist(brewery='Angry Erik')
        assert not status

    def test_AngryErikPage_ssml(self):
        angry_erik_page = AngryErikPage(mocked=True)
        assert angry_erik_page is not None
        status = angry_erik_page.fetch_taplist(brewery='Angry Erik')
        assert not status
        ssml = angry_erik_page.ssml_taplist()
        assert ssml
        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + angry_erik_page._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, mode='r', encoding='utf8')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == ssml  # anything different, raise hell!
