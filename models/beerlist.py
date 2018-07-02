from lxml import html
import requests
import bs4 as bs


# embodies everything we know about this beer
class Beer():
    _name = None
    _style = None
    _abv = None
    _hops = None

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name')
        self._style = kwargs.get('style')
        self._abv = kwargs.get('abv')
        self._hops = kwargs.get('hops')


# a list of beers
class BeerList(list):

    def append(self, beer: Beer) -> None:
        list.append(self, beer)


class BreweryPage():
    _url = None
    _cached_response = None
    _soup = None
    _beer_list = BeerList()
    _brewery_name = None

    def __init__(self, *args, **kwargs) -> None:
        self._url = kwargs.get('url')
        self._brewery_name = kwargs.get('brewery')

    def read(self, session = None) -> bool:
        assert(self._url is not None)
        if session is None:
            session = requests.Session()
        rsp = session.get(self._url)
        assert(rsp is not None)
        self._soup = bs.BeautifulSoup(rsp.text, 'lxml')
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
        beer_str = 'on tap at ' + self._brewery_name
        if not self._beer_list:
            return beer_str + "no beers listed"

        # okay, we have some beers, so iterate through them
        vowels = "aeiou"
        for beer in self._beer_list:
            beer_str += ' ' + beer._name
            if beer._style is not None:
                if beer._style[0].lower() in vowels:
                    beer_str += ", an " + beer._style
                else:
                    beer_str += ", a " + beer._style
            if beer._abv is not None:
                beer_str += " that is " + beer._abv + " alcohol"
            if beer._hops is not None:
                beer_str += " hopped with " + beer._hops
            beer_str +="."

        return beer_str

