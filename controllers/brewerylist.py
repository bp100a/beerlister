"""This is where we stash our brewery objects so they are all
in one place. Each brewery page needs to add itself to the global
list created at the end of this file."""
from typing import Tuple
import models.breweries.beerlist


class BreweryLister:
    """This is our controller for the brewery list"""
    brewery_page_list = []

    def add_brewery_page(self, brewerypage: models.breweries.beerlist.BreweryPage) -> None:
        """Adds a brewery page to the list we are managing"""
        self.brewery_page_list.append(brewerypage)

    def find_brewery(self, brewery_name) -> Tuple[models.breweries.beerlist.BreweryPage, str]:
        """finds a brewery page in the list we are managing"""
        # look for the specified brewery in our list of breweries we know about
        for brewery_page in self.brewery_page_list:
            brewery_id = brewery_page.brewery_by_alias(brewery_name)
            if brewery_id is not None:
                return brewery_page, brewery_id

        return None, None

    def list_of_breweries(self):
        """retrieve a list of all breweries by short name"""
        all_breweries = []
        for brewery_page in self.brewery_page_list:
            brewery_short_name = brewery_page.short_name()
            all_breweries.extend(brewery_short_name)

        # now we have a complete list of breweries
        return all_breweries

    # pylint: disable=C0200
    def ssml_brewery_list(self):
        """create the SSML to speak the list of breweries we know about"""
        list_of_breweries = self.list_of_breweries()
        resp = 'Here are the breweries I know: '
        for i in range(len(list_of_breweries)):
            if i == len(list_of_breweries) - 1:
                resp = resp + 'and ' + list_of_breweries[i]
            else:
                resp = resp + list_of_breweries[i] + ', '

        return resp
#
# initialize a "global" so all brewerypages can add themselves to this list
#


BREWERY_PAGES = BreweryLister()
