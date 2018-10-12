from unittest import TestCase
from tests.setupmocking import TestwithMocking
from models import cloudredis
import fakeredis
from models.breweries import *
from controllers import brewerylist


class TestBreweryList(TestwithMocking):
    """everything we need to test our our list of breweries"""

    def test_brewery_list(self):
        """ Test that all know brewery objects are listed in the global variable brewery_page_list"""
        brewery_page_objects = ["<class \'models.breweries.departedsoles.DepartedSolespage\'>",
                                "<class \'models.breweries.untappd.UnTappdPage\'>",
                                "<class \'models.breweries.twinelephant.TEBpage\'>",
                                "<class \'models.breweries.beermenus.BeerMenusPage\'>",
                                "<class \'models.breweries.digitalpour.DigitalPourPage\'>",
                                "<class \'models.breweries.jerseygirl.JerseyGirlPage\'>",
                                "<class \'models.breweries.angryerik.AngryErikPage\'>",
                                "<class \'models.breweries.traprock.TrapRockPage\'>"]

        for brewery in brewerylist.BREWERY_PAGES.brewery_page_list:
            bobj = str(type(brewery))
            if bobj not in brewery_page_objects:
                assert bobj in brewery_page_objects

    def test_find_breweries(self):
        """Test that all known breweries and their alias can be properly found in the global brewery_page_list"""
        # first define a list of breweries we should find
        known_breweries = {"Twin Elephant" : "<class \'models.breweries.twinelephant.TEBpage\'>",
                           "TEB": "<class \'models.breweries.twinelephant.TEBpage\'>",
                           "Twin Elephant Brewing": "<class \'models.breweries.twinelephant.TEBpage\'>",
                           "Twin Elephant Brewery": "<class \'models.breweries.twinelephant.TEBpage\'>",

                           "Departed Soles" : "<class \'models.breweries.departedsoles.DepartedSolespage\'>",
                           "Departed Soles Brewing": "<class \'models.breweries.departedsoles.DepartedSolespage\'>",
                           "Departed Soles Brewery": "<class \'models.breweries.departedsoles.DepartedSolespage\'>",

                           "Man Skirt" : "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Man Skirt Brewing" : "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Man Skirt Brewery" : "<class \'models.breweries.untappd.UnTappdPage\'>",

                           "Alementary": "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Alementary Brewing": "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Alementary Brewery": "<class \'models.breweries.untappd.UnTappdPage\'>",

                           "Angry Erik" : "<class \'models.breweries.angryerik.AngryErikPage\'>",
                           "Angry Erik Brewing": "<class \'models.breweries.angryerik.AngryErikPage\'>",
                           "Angry Erik Brewery": "<class \'models.breweries.angryerik.AngryErikPage\'>",

                           "Fort Nonsense": "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Fort Nonsense Brewing": "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Fort Nonsense Brewery": "<class \'models.breweries.untappd.UnTappdPage\'>",

                           "Demented" : "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Demented Brewing" : "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Demented Brewery" : "<class \'models.breweries.untappd.UnTappdPage\'>",

                           "Rinn Duin": "<class \'models.breweries.beermenus.BeerMenusPage\'>",
                           "Rinn Duin Brewing": "<class \'models.breweries.beermenus.BeerMenusPage\'>",
                           "Rinn Duin Brewery": "<class \'models.breweries.beermenus.BeerMenusPage\'>",

                           "Village Idiot": "<class \'models.breweries.digitalpour.DigitalPourPage\'>",
                           "Village Idiot Brewing": "<class \'models.breweries.digitalpour.DigitalPourPage\'>",
                           "Village Idiot Brewery": "<class \'models.breweries.digitalpour.DigitalPourPage\'>",

                           "Jersey Girl": "<class \'models.breweries.jerseygirl.JerseyGirlPage\'>",
                           "Jersey Girl Brewing": "<class \'models.breweries.jerseygirl.JerseyGirlPage\'>",
                           "Jersey Girl Brewery": "<class \'models.breweries.jerseygirl.JerseyGirlPage\'>"

                           }

        for brewery_alias in known_breweries:
            brewery_obj, brewery_id = brewerylist.BREWERY_PAGES.find_brewery(brewery_alias)
            assert str(type(brewery_obj)) == known_breweries[brewery_alias]
            assert brewery_id is not None

    def test_nobrewery(self):
        """Test that an unknown brewery is probably flagged"""
        brewery_obj, brewery_id = brewerylist.BREWERY_PAGES.find_brewery("no such brewery")
        assert brewery_obj is None and brewery_id is None

    def test_list_of_breweries(self):
        """Test that known breweries conform to the # we expect"""
        list_of_breweries = brewerylist.BREWERY_PAGES.list_of_breweries()
        assert len(list_of_breweries) == 11

    def test_list_of_breweries_response(self):
        """Test that we can generate an SSML for the list of known breweries"""
        resp = brewerylist.BREWERY_PAGES.ssml_brewery_list()
        assert resp is not None

    def test_set_home_brewery(self):
        """set a home brewery"""
        user_id = "amzn1.ask.account.AE53V7JF7U5ZCQHJTUYDLHKNKIP23LBVJVA4UISZUZBMUP7APYXL4WINBAFUFO647ZCWWR7ECPWV7YGPQPITT7X5FULYHALENOJ5XQC75TEELCTXA332I2POGQFEUYKFRU7EGSFBQPKBM22YENJVVTUR2XNX2P7S7O6I3SKXFJE4XJ2GJZ4WXKP7YIOSRNGZGNJECFEJIN5XELY"

        brewery = 'Twin Elephant'

        # first ensure there's not "home" brewery
        assert brewerylist.BREWERY_PAGES.get_home_brewery(user_id) is None

        # now set a "home" brewery
        assert brewerylist.BREWERY_PAGES.add_home_brewery(brewery_name=brewery, user_id=user_id)

        # now check we have a "home" brewery
        home_brewery = brewerylist.BREWERY_PAGES.get_home_brewery(user_id).decode('utf-8')
        assert home_brewery is not None and home_brewery == brewery

    def test_set_bad_home_brewery(self):
        """set a home brewery"""
        user_id = "amzn1.ask.account.AE53V7JF7U5ZCQHJTUYDLHKNKIP23LBVJVA4UISZUZBMUP7APYXL4WINBAFUFO647ZCWWR7ECPWV7YGPQPITT7X5FULYHALENOJ5XQC75TEELCTXA332I2POGQFEUYKFRU7EGSFBQPKBM22YENJVVTUR2XNX2P7S7O6I3SKXFJE4XJ2GJZ4WXKP7YIOSRNGZGNJECFEJIN5XELY"

        brewery = 'bogus brewery'

        # now set a bogus "home" brewery
        assert not brewerylist.BREWERY_PAGES.add_home_brewery(brewery_name=brewery, user_id=user_id)

