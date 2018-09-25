"""Unit tests for beer & beerlist"""
from unittest import TestCase
import models.breweries.beerlist
from tests.setupfakeredis import TestwithFakeRedis


class TestBeerList(TestwithFakeRedis):
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
