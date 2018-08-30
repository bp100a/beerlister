import requests
import bs4 as bs
import re

# embodies everything we know about this beer
class Beer():
    _name = None
    _style = None
    _abv = None
    _hops = []
    _ibu = None
    _desc = None

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name')
        self._style = kwargs.get('style')
        self._abv = kwargs.get('abv')
        if kwargs.get('ibu') is not None:
            self._ibu = kwargs.get('ibu')
        if kwargs.get('desc') is not None:
            self._desc = kwargs.get('desc')
        if kwargs.get('hops') is not None:
            self._hops = re.split('& |, ', kwargs.get('hops'))


# a list of beers
class BeerList(list):

    def append(self, beer: Beer) -> None:
        list.append(self, beer)


class BreweryPage():

    def __init__(self, *args, **kwargs) -> None:
        self._url = kwargs.get('url')
        self._brewery_name = kwargs.get('brewery')
        self._include_hops = kwargs.get('hops')
        self._beer_list = BeerList()
        self._soup = None
        self._cached_response = None

    def read(self, session = None) -> bool:
        assert(self._url is not None)
        if session is None:
            session = requests.Session()
        rsp = session.get(self._url)
        assert(rsp is not None)
        self._soup = bs.BeautifulSoup(rsp.text, "html.parser")
        session.close()
        self._cached_response = rsp
        return self._soup is not None

    def add_beer(self, beer: Beer) -> None:
        self._beer_list.append(beer)

    def get_beerlist(self) -> BeerList:
        return self._beer_list

    def alexa_taplist(self) -> str:
        # create a string for the tap list we have
        assert(self._beer_list is not None)
        assert(self._brewery_name is not None)
        beer_str = 'on tap at ' + self._brewery_name + '<break strength="strong"/>'
        if not self._beer_list:
            return beer_str + "no beers listed"

        # okay, we have some beers, so iterate through them
        vowels = "aeiou"
        for beer in self._beer_list:
            beer_str += ' ' + beer._name.replace('IT', '<sub alias="it"> IT </sub>')

            if beer._style is not None:
                beer_style = beer._style.replace(' IPA', ' <say-as interpret-as="spell-out">IPA</say-as>')
                beer_style = beer_style.replace(' DIPA', ' double <say-as interpret-as="spell-out">IPA</say-as>')
                if beer._style[0].lower() in vowels:
                    beer_str += ", an " + beer_style
                else:
                    beer_str += ", a " + beer_style
            if beer._abv is not None:
                beer_str += " that is " + beer._abv + " alcohol"
            if len(beer._hops) > 0:
                beer_str += ", hopped with "
                if len(beer._hops) == 1:
                    beer_str += beer._hops[0]
                else:
                    beer_str += "{} and {}".format(", ".join(beer._hops[:-1]),  beer._hops[-1])

            beer_str +="."

        return beer_str

