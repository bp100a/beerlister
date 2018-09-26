"""brewery page to web scrape departed soles website for tap list"""
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class DepartedSolespage(BreweryPage):
    """scrape website of Departed Soles Brewing, Jersey City"""
    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Departed Soles" : ["Departed Soles Brewing", "Departed Soles Brewery"]}

    def fetch_taplist(self, **kwargs) -> None:
        """fetch the taplist page for Departed Soles and parse it"""
        BreweryPage.fetch_taplist(self, url="http://www.departedsoles.com/beer.html", **kwargs)
        assert self._url is not None
        self.read_page(brewery=list(self._alias.keys())[0])  # read the page
        beer_div_list = self._soup.find_all("div", {"class": "beersamples"})
        for beer in beer_div_list:
            name = None
            style = None
            abv = None
            if beer.contents[1].name == 'h4':
                name = beer.contents[1].text
                style = beer.contents[3].text.split(u'\u2022')[0].strip()
                abv = beer.contents[3].text.split(u'\u2022')[1].strip()
                # now add the beer to the list
                self.add_beer(Beer(name=name, style=style, abv=abv, hops=None))

        # we now have a list of beers for this brewery
        assert self._beer_list is not None


# add this to the list of breweries
# Note: Don't add departed soles, talked to brewer and it's not
#       up to date.
# brewerylist.BREWERY_PAGES.add_brewery_page(DepartedSolespage())
