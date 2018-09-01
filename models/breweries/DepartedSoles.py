from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist

class DepartedSolespage(BreweryPage):
    # Departed Soles Brewing, Jersey City NJ

    def fetch_taplist(self, *args, **kwargs) -> None:
        BreweryPage.fetch_taplist(self, url="http://www.departedsoles.com/beer.html", brewery="Departed Soles", **kwargs)
        assert(self._url is not None)
        self.read_page() # read the page
        assert(self._cached_response is not None)
        assert(self._soup is not None)
        beer_div_list = self._soup.find_all("div", {"class": "beersamples"})
        assert(beer_div_list is not None)
        for beer in beer_div_list:
            assert(beer is not None)
            name = None
            style = None
            abv = None
            hops = None
            if beer.contents[1].name == 'h4':
                name = beer.contents[1].text
                style = beer.contents[3].text.split(u'\u2022')[0].strip()
                abv = beer.contents[3].text.split(u'\u2022')[1].strip()
                # now add the beer to the list
                self.add_beer(Beer(name=name, style=style, abv=abv, hops=hops) )

        # we now have a list of beers for this brewery
        assert(self._beer_list is not None)

# add this to the list of breweries
brewerylist.brewery_pages.add_brewery_page(DepartedSolespage())