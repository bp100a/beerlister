import models.breweries.beerlist
from typing import Tuple


class BreweryLister:

    brewery_page_list = []

    def add_brewery_page(self, brewerypage : models.breweries.beerlist.BreweryPage) -> None:
        self.brewery_page_list.append(brewerypage)

    def find_brewery(self, brewery_name) -> Tuple[models.breweries.beerlist.BreweryPage, str]:
        # look for the specified brewery in our list of breweries we know about
        for breweryPage in self.brewery_page_list:
            brewery_id = breweryPage.brewery_by_alias(brewery_name)
            if brewery_id is not None:
                return breweryPage, brewery_id

        return None, None

    def list_of_breweries(self):

        all_breweries = []
        for breweryPage in self.brewery_page_list:
            bl = breweryPage.short_name()
            all_breweries.extend(bl)

        # now we have a complete list of breweries
        return all_breweries

    def ssml_brewery_list(self):

        bl = self.list_of_breweries()
        resp = 'Here are the breweries I know: '
        for i in range(len(bl)):
            if i == len(bl) - 1:
                resp = resp + 'and ' + bl[i]
            else:
                resp = resp + bl[i] + ', '

        return resp
#
# initialize a "global" so all brewerypages can add themselves to this list
#
brewery_pages = BreweryLister()
