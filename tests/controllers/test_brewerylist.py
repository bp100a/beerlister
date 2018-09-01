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
