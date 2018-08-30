from models.beerlist import BreweryPage
from models.beerlist import Beer
import string

class DepartedSolespage(BreweryPage):
    # Departed Soles Brewing, Jersey City NJ

    def __init__(self) -> None:
        BreweryPage.__init__(self, url="http://www.departedsoles.com/beer.html", brewery="Departed Soles")
        assert(self._url is not None)
        self.read() # read the page
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
                style = beer.contents[3].text.split(u'\xe2\x80\xa2')[0]
                abv = beer.contents[3].text.split(u'\xe2\x80\xa2')[1]
                # now add the beer to the list
                self.add_beer(Beer(name=name, style=style, abv=abv, hops=hops) )

        # we now have a list of beers for this brewery
        assert(self._beer_list is not None)