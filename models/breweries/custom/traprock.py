"""brewery page to web scrape departed soles website for tap list"""

import re
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class TrapRockPage(BreweryPage):
    """scrape website of Trap Rock Brewery, Berkley Heights"""

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {
            "Trap Rock": ["Trap Rock Brewing", "Trap Rock Brewery", "track rock"]
        }

    def parse_beer(self, div) -> None:
        """
        this is our <div> that encapsulates a beer
        """
        beer_name = div.contents[0]
        beer_description = div.nextSibling.text
        abv_pos = beer_description.rfind(";")
        beer_style: str = ""
        beer_abv = None
        if abv_pos != -1:
            beer_style = beer_description[:abv_pos]
            beer_abv = beer_description[abv_pos + 1 :]

        if beer_name and beer_abv:
            self.add_beer(
                Beer(name=beer_name, style=beer_style, abv=beer_abv, hops=None)
            )

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch the taplist page for Angry Erik and parse it"""
        BreweryPage.fetch_taplist(
            self, url="http://www.traprockrestaurant.net/menus/8449", **kwargs
        )
        assert self._url is not None
        is_cached = self.read_page(brewery=list(self._alias.keys())[0])  # read the page
        if is_cached:
            return True

        div_list = self._soup.find_all("div", {"class": "menu-item-name"})
        for div in div_list:
            if "32oz" in div.text:
                continue
            self.parse_beer(div)

        return False  # not from cache


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(TrapRockPage())
