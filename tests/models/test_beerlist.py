"""Unit tests for beer & beerlist"""
from tests.setupmocking import TestwithMocking
import models.breweries.beerlist
from models import cloudredis
import fakeredis


class TestBeerList(TestwithMocking):
    """quick tests on the beer object & list"""

    @staticmethod
    def test_add_empty_beer():
        """Test that we can create a beer list and add an empty beer"""
        beer_list = models.breweries.beerlist.BeerList()
        assert beer_list is not None

        beer = models.breweries.beerlist.Beer()
        assert beer.name is None
        assert beer.style is None
        assert beer.abv is None
        assert beer.hops is not None
        assert not beer.hops

        assert beer.has_hops() is False

        beer_list.append(beer)
        assert len(beer_list) == 1

    @staticmethod
    def test_add_full_beer():
        """add a beer with all attributes"""
        beer_list = models.breweries.beerlist.BeerList()
        assert beer_list is not None

        beer = models.breweries.beerlist.Beer(name='Budweiser', style='Bohemian Lager',
                                              abv='4.0%', hops='Citra, Cascade')
        assert beer.name is not None
        assert beer.style is not None
        assert beer.abv is not None
        assert beer.hops is not None

        assert len(beer.hops) == 2

        beer_list.append(beer)
        assert len(beer_list) == 1

    @staticmethod
    def test_hops_array():
        """test that we can manage our hops array"""
        beer = models.breweries.beerlist.Beer()
        assert beer.has_hops() is False

        beer = models.breweries.beerlist.Beer(name='Budweiser', style='Bohemian Lager',
                                              abv='4.0%', hops='Citra, Cascade')
        assert beer.has_hops() is True

    @staticmethod
    def test_IPA_style():
        """test that when IPA is in a beer style, it's handled properly"""
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "IPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Sculpin', style='American IPA',
                                              abv='4.0%', hops='Citra, Cascade')
        brewery_page.add_beer(beer)
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert '<say-as interpret-as="spell-out">IPA</say-as>' in ssml_taplist

    @staticmethod
    def test_IPA_name():
        """test that when IPA is in a beer style, it's handled properly"""
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "IPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Sculpin IPA', style='American Ale',
                                              abv='4.0%', hops='Citra, Cascade')
        brewery_page.add_beer(beer)
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert '<say-as interpret-as="spell-out">IPA</say-as>' in ssml_taplist

    @staticmethod
    def test_DIPA_style():
        """test that when IPA is in a beer style, it's handled properly"""
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "DIPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Nimble Giant', style='American DIPA',
                                              abv='4.0%', hops='Citra, Cascade')
        brewery_page.add_beer(beer)
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert 'double <say-as interpret-as="spell-out">IPA</say-as>' in ssml_taplist

    @staticmethod
    def test_DIPA_name():
        """test that when IPA is in a beer style, it's handled properly"""
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "DIPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Nimble Giant DIPA', style='American Ale',
                                              abv='4.0%', hops='Citra, Cascade')
        brewery_page.add_beer(beer)
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert 'double <say-as interpret-as="spell-out">IPA</say-as>' in ssml_taplist

    @staticmethod
    def test_NewEngland_IPA_style():
        """test that when IPA is in a beer style, it's handled properly"""
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "NEIPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Heady Topper', style='NEIPA',
                                              abv='4.0%', hops='Citra, Cascade')
        brewery_page.add_beer(beer)
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert 'New England <say-as interpret-as="spell-out">IPA</say-as>' in ssml_taplist

    @staticmethod
    def test_NewEngland_IPA_name():
        """test that when IPA is in a beer style, it's handled properly"""
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "NEIPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Heady Topper NEIPA', style='New England Ale',
                                              abv='4.0%', hops='Citra, Cascade')
        brewery_page.add_beer(beer)
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert 'New England <say-as interpret-as="spell-out">IPA</say-as>' in ssml_taplist

    @staticmethod
    def test_no_beers():
        fake = fakeredis.FakeStrictRedis()
        cloudredis.initialize_cloud_redis(injected_server=fake)

        brewery_page = models.breweries.beerlist.BreweryPage(mocked=False)
        brewery_page._brewery_name = "NEIPA brewery"
        brewery_page._beer_list = models.breweries.beerlist.BeerList()
        brewery_page._cached_response = "bogus html page"

        beer = models.breweries.beerlist.Beer(name='Heady Topper NEIPA', style='New England Ale',
                                              abv='4.0%', hops='Citra, Cascade')
        ssml_taplist = brewery_page.ssml_taplist()
        assert ssml_taplist is not None
        assert 'no beers listed' in ssml_taplist