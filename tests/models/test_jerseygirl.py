from unittest import TestCase
import os
from models.breweries.jerseygirl import JerseyGirlPage
from tests.models.common import data_dir
from tests.setupfakeredis import TestwithFakeRedis


class TestJerseyGirlpage(TestwithFakeRedis):

    def live_JerseyGirl_read(self):
        jerseygirl = JerseyGirlPage(mocked=False)
        assert jerseygirl is not None
        jerseygirl.fetch_taplist(brewery="Jersey Girl")

    def test_parse_abv_style(self):
        jg_abv_style = [{'text': 'ABV- 10.0% Belgian Tripel', 'abv': '10.0%', 'style': 'Belgian Tripel'},
                        {'text': '7.5% ABV - West Coast Style IPA', 'abv': '7.5%', 'style': 'West Coast Style IPA'},
                        {'text': 'ABV: 6.2% - French Saison', 'abv': '6.2%', 'style': 'French Saison'},
                        {'text': 'ABV - 6.5% - New England Style IPA', 'abv': '6.5%', 'style': 'New England Style IPA'},
                        {'text': 'ABV 4.5% - Traditional, German-style Pilsner', 'abv': '4.5%', 'style': 'Traditional, German-style Pilsner'},
                        {'text': 'ABV: 4.0% - Hefeweizen', 'abv': '4.0%', 'style': 'Hefeweizen'}]
        jerseygirl = JerseyGirlPage(mocked=True)

        for style_string in jg_abv_style:
            abv, style = jerseygirl.parse_content(style_string['text'])
            assert abv == style_string['abv']
            assert style == style_string['style']


    def test_JerseyGirl_beerlist(self):
        """Test we can read the Twin Elephant beer list!"""
        jerseygirl_page = JerseyGirlPage(mocked=True)
        assert jerseygirl_page is not None
        jerseygirl_page.fetch_taplist(brewery="Jersey Girl")
        beer_string = jerseygirl_page.ssml_taplist()
        assert beer_string is not None

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        file_name = data_dir() + jerseygirl_page._brewery_name.replace(' ', '') + '.SSML'
        file_pointer = open(file_name, mode='r', encoding='utf8')
        tst_data = file_pointer.read()
        file_pointer.close()
        assert tst_data == beer_string  # anything different, raise hell!

    def test_JerseyGirl_cached(self):
        """Test we can read the Twin Elephant beer list!"""
        jerseygirl_page = JerseyGirlPage(mocked=True)
        assert jerseygirl_page is not None
        from_cache = jerseygirl_page.fetch_taplist(brewery="Jersey Girl")
        assert not from_cache

        # 2nd read from cache!
        jerseygirl_page.ssml_taplist() # this puts it in the cache
        from_cache = jerseygirl_page.fetch_taplist(brewery="Jersey Girl")
        assert from_cache
