import models.breweries.beerlist
from typing import Tuple

class BreweryLister():

    brewery_page_list = []
    def add_brewery_page(self, brewerypage : models.breweries.beerlist.BreweryPage) -> None:
        self.brewery_page_list.append(brewerypage)

    def find_brewery(self, brewery_name) -> Tuple[models.breweries.beerlist.BreweryPage, str]:
        # look for the specified brewery in our list of breweries we know about
        for breweryPage in self.brewery_page_list:
            brewery_id = breweryPage.brewery_by_alias(brewery_name)
            if brewery_id is not None:
                return breweryPage, brewery_id

        return ((),)

# initialize a "global" so all brewerypages can add themselves to this list
brewery_pages = BreweryLister()
