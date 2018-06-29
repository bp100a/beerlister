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
class BeerList():
    _list = []

    def add(self, beer: Beer) -> None:
        self._list.append(beer)


class BreweryPage():
    _url = None
    _cached_response = None
    _soup = None
    _beer_list = None

    def __init__(self, *args, **kwargs):
        self._url = kwargs.get('url')
        self._beer_list = BeerList()

    def read(self, session = None):
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
        self._beer_list.add(beer)
