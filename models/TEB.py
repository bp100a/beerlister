from models.beerlist import BreweryPage
from models.beerlist import Beer
import string

class TEBpage(BreweryPage):
    # Twin Elephant Brewing Company, Chatham NJ
    # main page has list of beers on tap:
    #
    # "beer-name"
    # "beer-style" (description is next
    # "ABV"
    # "OG"
    # "COLOR:"
    # "MALT:"
    # "HOPS:"
    # "YEAST:"
    # "Misc:"

    def __init__(self) -> None:
        BreweryPage.__init__(self, url="https://www.twinelephant.com", brewery="Twin Elephant")
        assert(self._url is not None)
        self.read() # read the page
        assert(self._cached_response is not None)
        assert(self._soup is not None)
        beer_div_list = self._soup.find_all("div", {"class": "beer-holder"})
        assert(beer_div_list is not None)
        for beer in beer_div_list:
            assert(beer is not None)
            name = None
            style = None
            abv = None
            hops = None
            for c in beer.contents:
                if hasattr(c, 'attrs'):
                    if (len(c.attrs) > 0):
                        if 'beer-name' in c.attrs['class']:
                            name = c.text
                        if 'beer-style' in c.attrs['class']:
                            style = c.text
                        if 'pure-g' in c.attrs['class']:   # ABV start
                            for inner_c in c.contents:
                                if hasattr(inner_c, 'attrs'):
                                    if 'pure-u-1' in inner_c.attrs['class']:
                                        # our string is "\nABV: 6.2%\n", we just want the '6.2%' portion
                                        if inner_c.text.find('ABV:') != -1:
                                            abv = inner_c.text.split('ABV:')[1].strip()
                                            assert(abv is not None)
                                        elif inner_c.text.find('HOPS:') != -1:
                                            hops = inner_c.text.split('HOPS:')[1].strip()
                                            assert(hops is not None)

            # now add the beer to the list
            self.add_beer(Beer(name=name, style=style, abv=abv, hops=hops) )

        # we now have a list of beers for this brewery
        assert(self._beer_list is not None)