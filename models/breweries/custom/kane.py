"""brewery page to web scrape departed soles website for tap list"""
import re
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class KanePage(BreweryPage):
    """scrape website of Departed Soles Brewing, Jersey City"""
    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Kane": ["Kane Brewing",
                                "Kane Brewery"]}

    @staticmethod
    def parse_beer_abv(tag) -> str:
        abv = tag.contents[3].contents[1].text.split('%')[0]
        return abv

    @staticmethod
    def parse_beer_style(tag) -> str:
        style = tag.contents[3].contents[0].strip("\n\t ").rstrip("/ ")
        return style

    @staticmethod
    def filter(tag) -> bool:
        if (tag.has_attr('class') and
            "panel" in tag.attrs['class'] and
                "product" in tag.attrs['class']) or \
                (tag.has_attr('id') and
                 ("beers-to-go" in tag.attrs['id'] or "beers-on-tap" in tag.attrs['id'])):
            return True

        return False

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch the taplist page for Kane Brewing and parse it
        We only display "On Premise" beers and not the one's that are
        permanent.
        """
        BreweryPage.fetch_taplist(self, url="http://www.kanebrewing.com", **kwargs)
        assert self._url is not None
        is_cached = self.read_page(brewery=list(self._alias.keys())[0])  # read the page
        if is_cached:
            return True

        tag_list = self._soup.find_all(KanePage.filter) #  find_all("div", {"class": "panel", "class": "product"})
        panel_idx = 0
        for tag in tag_list:
            if "panel-two-column" in tag['class']:
                panel_idx += 1
                if panel_idx > 1:
                    break
            else:
                beer_name = tag.contents[1].text.strip("\n ")
                beer_style = KanePage.parse_beer_style(tag)
                beer_abv = KanePage.parse_beer_abv(tag)
                if len(tag.contents) > 5:
                    beer_desc = tag.contents[5].text.strip("\n ")
                    self.add_beer(Beer(name=beer_name,
                                       style=beer_style,
                                       abv=beer_abv,
                                       desc=beer_desc,
                                       hops=None))

        return False # not from cache


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(KanePage())
