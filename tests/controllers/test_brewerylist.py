from unittest import TestCase
from controllers import brewerylist # for clarity
from models.breweries import *



class TestBreweryList(TestCase):

    def test_brewery_list(self):
        brewery_page_objects = ["<class \'models.breweries.DepartedSoles.DepartedSolespage\'>",
                                "<class \'models.breweries.untappd.UnTappdPage\'>",
                                "<class \'models.breweries.TEB.TEBpage\'>",
                                "<class \'models.breweries.beermenus.BeerMenusPage\'>",
                                "<class \'models.breweries.digitalpour.DigitalPourPage\'>"]
        for brewery in brewerylist.brewery_pages.brewery_page_list:
            object = str(type(brewery))
            assert(object in brewery_page_objects)

    def test_find_breweries(self):
        # first define a list of breweries we should find
        known_breweries = {"Twin Elephant" : "<class \'models.breweries.TEB.TEBpage\'>",
                           "TEB": "<class \'models.breweries.TEB.TEBpage\'>",
                           "Twin Elephant Brewing": "<class \'models.breweries.TEB.TEBpage\'>",
                           "Twin Elephant Brewery": "<class \'models.breweries.TEB.TEBpage\'>",

                           "Departed Soles" : "<class \'models.breweries.DepartedSoles.DepartedSolespage\'>",
                           "Departed Soles Brewing": "<class \'models.breweries.DepartedSoles.DepartedSolespage\'>",
                           "Departed Soles Brewery": "<class \'models.breweries.DepartedSoles.DepartedSolespage\'>",

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
            brewery_obj = brewerylist.brewery_pages.find_brewery(brewery_alias)
            assert(str(type(brewery_obj)) == known_breweries[brewery_alias])
