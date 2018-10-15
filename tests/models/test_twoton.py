import os
from models.breweries.twoton import TwoTonPage
from tests.models.common import data_dir
from tests.setupmocking import TestwithMocking


class ContentTest():
    name = None
    text = None


class ContentNoNameTest():
    text = None


class DivTest():
    contents = []


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

    def test_TwoTonPage_div_not_content(self):
        twoton_page = TwoTonPage(mocked=True)

        div_no_contents = {"div_no_contents": 'dummy'}
        assert not twoton_page.parse_beer(div_no_contents)

    def test_TwoTonPage_div_content_no_name(self):
        twoton_page = TwoTonPage(mocked=True)
        div_no_name = DivTest()
        contents = ContentNoNameTest()
        div_no_name.contents.append(contents)
        assert not twoton_page.parse_beer(div_no_name)

    def test_TwoTonPage_div_content_name_not_h2(self):
        twoton_page = TwoTonPage(mocked=True)
        div_not_h2 = DivTest()
        contents = ContentTest()
        div_not_h2.contents.append(contents)
        div_not_h2.contents[0].name = 'not h2'
        assert not twoton_page.parse_beer(div_not_h2)

    def test_TwoTonPage_div_text_not_ABV(self):
        twoton_page = TwoTonPage(mocked=True)

        div_not_abv = DivTest()
        contents = ContentTest()
        div_not_abv.contents.append(contents)
        div_not_abv.contents[0].name = 'h2'
        div_not_abv.contents[0].text = 'not A.B.V.'
        assert not twoton_page.parse_beer(div_not_abv)

    def test_TwoTonPage_cached(self):
        """Test we can read the Twin Elephant beer list!"""
        TwoTon_page = TwoTonPage(mocked=True)
        from_cache = TwoTon_page.fetch_taplist(brewery="TwoTon")
        assert not from_cache

        # 2nd read from cache!
        TwoTon_page.ssml_taplist() # this puts it in the cache
        from_cache = TwoTon_page.fetch_taplist(brewery="TwoTon")
        assert from_cache
