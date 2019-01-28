from unittest import TestCase
import os
from models.breweries.custom.kane import KanePage
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class TestKanepage(TestwithMocking):

    def test_Kane_read(self):
        kane = KanePage(mocked=True)
        assert kane is not None
        kane.fetch_taplist(brewery="Kane")

    def test_KanePage_ssml(self):
        kane_page = KanePage(mocked=True)
        assert kane_page is not None
        status = kane_page.fetch_taplist(brewery='Kane')
        assert not status
        ssml = kane_page.ssml_taplist()
        assert ssml
        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + kane_page._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, mode='r', encoding='utf8')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == ssml  # anything different, raise hell!

    def test_KanePage_cached(self):
        """Test we can read the Kane beer list!"""
        kane_page = KanePage(mocked=True)
        from_cache = kane_page.fetch_taplist(brewery="Kane")
        assert not from_cache

        # 2nd read from cache!
        kane_page.ssml_taplist() # this puts it in the cache
        from_cache = kane_page.fetch_taplist(brewery="Kane")
        assert from_cache
