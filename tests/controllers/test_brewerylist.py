from unittest import TestCase
from controllers import brewerylist  # for clarity
from models.breweries import *


class TestBreweryList(TestCase):
    """everything we need to test our our list of breweries"""

    def test_brewery_list(self):
        """ Test that all know brewery objects are listed in the global variable brewery_page_list"""
        brewery_page_objects = ["<class \'models.breweries.departedsoles.DepartedSolespage\'>",
                                "<class \'models.breweries.untappd.UnTappdPage\'>",
                                "<class \'models.breweries.twinelephant.TEBpage\'>",
                                "<class \'models.breweries.beermenus.BeerMenusPage\'>",
                                "<class \'models.breweries.digitalpour.DigitalPourPage\'>"]
        for brewery in brewerylist.BREWERY_PAGES.brewery_page_list:
            bobj = str(type(brewery))
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

                           "Angry Erik" : "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Angry Erik Brewing": "<class \'models.breweries.untappd.UnTappdPage\'>",
                           "Angry Erik Brewery": "<class \'models.breweries.untappd.UnTappdPage\'>",

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
                           "Village Idiot Brewery": "<class \'models.breweries.digitalpour.DigitalPourPage\'>"
                           }

        for brewery_alias in known_breweries:
            brewery_obj, brewery_id = brewerylist.BREWERY_PAGES.find_brewery(brewery_alias)
            assert str(type(brewery_obj)) == known_breweries[brewery_alias]
            assert brewery_id is not None

    def test_brewerylist(self):
        """We will clearn the brewery list then manually add all known objects, then verify"""
        # clear the brewerylist
        brewerylist.BREWERY_PAGES.brewery_page_list = []
        brewerylist.BREWERY_PAGES.add_brewery_page(twinelephant.TEBpage())
        brewerylist.BREWERY_PAGES.add_brewery_page(departedsoles.DepartedSolespage())
        brewerylist.BREWERY_PAGES.add_brewery_page(digitalpour.DigitalPourPage())
        brewerylist.BREWERY_PAGES.add_brewery_page(beermenus.BeerMenusPage())
        brewerylist.BREWERY_PAGES.add_brewery_page(untappd.UnTappdPage())

        # now that we added them, see if they are there
        self.test_find_breweries()

    def test_nobrewery(self):
        """Test that an unknown brewery is probably flagged"""
        brewery_obj, brewery_id = brewerylist.BREWERY_PAGES.find_brewery("no such brewery")
        assert brewery_obj is None and brewery_id is None

    def test_list_of_breweries(self):
        """Test that known breweries conform to the # we expect"""
        list_of_breweries = brewerylist.BREWERY_PAGES.list_of_breweries()
        assert len(list_of_breweries) == 9

    def test_list_of_breweries_response(self):
        """Test that we can generate an SSML for the list of known breweries"""
        resp = brewerylist.BREWERY_PAGES.ssml_brewery_list()
        assert resp is not None
