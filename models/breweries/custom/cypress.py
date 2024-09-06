"""brewery page to web scrape Cypress website for tap list"""

from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class CypressPage(BreweryPage):
    """scrape website of Trap Rock Brewery, Berkley Heights"""

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Cypress": ["Cypress Brewing", "Cypress Brewery"]}

    def parse_beer(self, div) -> bool:
        """
        this is our encapsulated a beer
        """
        if not hasattr(div, "contents"):
            return False

        beer_name = div.contents[1].text
        parts = div.contents[3].text.split()
        beer_abv = parts[1]
        beer_style = div.contents[5].text
        if not beer_name or not beer_abv:
            return False

        # if we have a name & abv, then add the beer to our list
        self.add_beer(Beer(name=beer_name, style=beer_style, abv=beer_abv, hops=None))
        return True

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch the taplist page for Cypress and parse it"""
        BreweryPage.fetch_taplist(
            self,
            url="http://cypressbrewing.com/beer_type/currently-available/",
            **kwargs
        )
        assert self._url is not None
        is_cached = self.read_page(brewery=list(self._alias.keys())[0])  # read the page
        if is_cached:
            return True

        div_list = self._soup.find_all("div", {"class": "menu-content-pro"})
        for div in div_list:
            self.parse_beer(div)

        return False  # not from cache


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(CypressPage())
