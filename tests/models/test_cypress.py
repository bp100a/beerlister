import os
from models.breweries.custom.cypress import CypressPage
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class TestCypressPage(TestwithMocking):
    """test for the departed soles web scraping page"""

    def test_CypressPage_read(self):
        """Test that we can do basic read of page"""
        cypress_page = CypressPage(mocked=True)
        assert cypress_page is not None
        status = cypress_page.fetch_taplist(brewery="Cypress")
        assert not status

    def test_CypressPage_ssml(self):
        cypress_page = CypressPage(mocked=True)
        assert cypress_page is not None
        status = cypress_page.fetch_taplist(brewery="Cypress")
        assert not status
        ssml = cypress_page.ssml_taplist()
        assert ssml
        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + cypress_page._brewery_name.replace(" ", "") + ".SSML"
        file_pointer = open(file_name, mode="r", encoding="utf8")
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == ssml  # anything different, raise hell!

    def test_CypressPage_cached(self):
        """Test we can read the Twin Elephant beer list!"""
        cypress_page = CypressPage(mocked=True)
        from_cache = cypress_page.fetch_taplist(brewery="Cypress")
        assert not from_cache

        # 2nd read from cache!
        cypress_page.ssml_taplist()  # this puts it in the cache
        from_cache = cypress_page.fetch_taplist(brewery="Cypress")
        assert from_cache

    def test_CypressPage_div_not_content(self):
        cypress_page = CypressPage(mocked=True)

        div_no_contents = {"div_no_contents": "dummy"}
        assert not cypress_page.parse_beer(div_no_contents)
