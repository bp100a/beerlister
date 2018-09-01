import models.breweries.beerlist

class BreweryLister():

    brewery_page_list = []
    def add_brewery_page(self, brewerypage):
        self.brewery_page_list.append(brewerypage)

brewery_pages = BreweryLister()
