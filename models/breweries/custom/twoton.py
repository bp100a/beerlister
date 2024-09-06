"""brewery page to web scrape Two Ton website for tap list"""

from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class TwoTonPage(BreweryPage):
    """scrape website of Trap Rock Brewery, Berkley Heights"""

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {
            "Two Ton": [
                "Two Ton Brewing",
                "Two Ton Brewery",
                "2 ton",
                "2 ton brewing",
                "2 ton brewery",
            ]
        }

    def parse_beer(self, div) -> bool:
        """
        this is our encapsulated a beer
        """
        if not hasattr(div, "contents"):
            return False
        if not hasattr(div.contents[0], "name"):
            return False
        if div.contents[0].name != "h2":
            return False
        if div.contents[0].text.find("ABV") == -1:
            return False
        try:
            parts = div.contents[0].text.split(" -")
            beer_name = parts[0].strip()
            beer_abv = parts[1][: parts[1].find("ABV")].strip()
        except IndexError:
            return False

        if not beer_name or not beer_abv:
            return False
        self.add_beer(Beer(name=beer_name, style=None, abv=beer_abv, hops=None))
        return True

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch the taplist page for Two Ton and parse it"""
        BreweryPage.fetch_taplist(
            self, url="http://www.twotonbrewing.com/beers/", **kwargs
        )
        assert self._url is not None
        is_cached = self.read_page(brewery=list(self._alias.keys())[0])  # read the page
        if is_cached:
            return True

        div_list = self._soup.find_all("div", {"class": "sqs-block-content"})
        for div in div_list:
            self.parse_beer(div)

        return False  # not from cache


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(TwoTonPage())
