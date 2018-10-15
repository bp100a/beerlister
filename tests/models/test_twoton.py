import os
from models.breweries.twoton import TwoTonPage
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class TestTwoTonPage(TestwithMocking):
    """test for the departed soles web scraping page"""

    def test_TwoTonPage_read(self):
        """Test that we can do basic read of page"""
        two_ton_page = TwoTonPage(mocked=True)
        assert two_ton_page is not None
        status = two_ton_page.fetch_taplist(brewery='Two Ton')
        assert not status

    def test_TwoTonPage_ssml(self):
        two_ton_page = TwoTonPage(mocked=True)
        assert two_ton_page is not None
        status = two_ton_page.fetch_taplist(brewery='Two Ton')
        assert not status
        ssml = two_ton_page.ssml_taplist()
        assert ssml
        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + two_ton_page._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, mode='r', encoding='utf8')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == ssml  # anything different, raise hell!
