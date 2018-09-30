""" Brewery Page to scrape Twin Elephants web site for a taplist"""
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class TEBpage(BreweryPage):
    """ Twin Elephant Brewing Company, Chatham NJ
     main page has list of beers on tap:

     "beer-name"
     "beer-style" (description is next
     "ABV"
     "OG"
     "COLOR:"
     "MALT:"
     "HOPS:"
     "YEAST:"
     "Misc:"
    """
    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Twin Elephant": ["TEB", "Twin Elephant Brewing", "Twin Elephant Brewery"]}

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch taplist for TEB, directly scraping their site and parsing"""

        # perform any pre-fetch initialization of base class
        BreweryPage.fetch_taplist(self, url="http://www.twinelephant.com", **kwargs)
        assert self._url is not None
        is_cached = self.read_page(brewery=list(self._alias.keys())[0]) # read the page
        if is_cached:
            return True

        beer_div_list = self._soup.find_all("div", {"class": "beer-holder"})
        for beer in beer_div_list:
            assert beer is not None
            name = None
            style = None
            abv = None
            hops = None
            for content in beer.contents:
                if hasattr(content, 'attrs'):
                    if content.attrs and 'class' in content.attrs:
                        if 'beer-name' in content.attrs['class']:
                            name = content.text
                        if 'beer-style' in content.attrs['class']:
                            style = content.text
                        if 'pure-g' in content.attrs['class']:   # ABV start
                            for inner_c in content.contents:
                                if hasattr(inner_c, 'attrs'):
                                    if 'pure-u-1' in inner_c.attrs['class']:
                                        # our string is "\nABV: 6.2%\n",
                                        # we just want the '6.2%' portion
                                        if inner_c.text.find('ABV:') != -1:
                                            abv = inner_c.text.split('ABV:')[1].strip()
                                            assert abv is not None
                                        elif inner_c.text.find('HOPS:') != -1:
                                            hops = inner_c.text.split('HOPS:')[1].strip()
                                            assert hops is not None

            # now add the beer to the list
            self.add_beer(Beer(name=name, style=style, abv=abv, hops=hops))

        # we now have a list of beers for this brewery
        assert self._beer_list is not None

        return False # not from cache

# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(TEBpage())
