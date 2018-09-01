import requests
import bs4 as bs
import re
import os
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

        if self._style is not None:
            self._style = self._style.replace(u'\xf6', 'o') # fix umla in Kolsch


# a list of beers
class BeerList(list):

    def append(self, beer: Beer) -> None:
        list.append(self, beer)


class BreweryPage():

    _url = None
    _brewery_name = None
    _soup = None
    _cached_response = None
    _beer_list = None
    _mocked = False
    _include_hops = True

    def __init__(self, *args, **kwargs) -> None:
        self._include_hops = kwargs.get('hops')
        self._mocked = kwargs.get('mocked', False)
        self._url = kwargs.get('url', None)

    def fetch_taplist(self, *args, **kwargs):
        self._beer_list = BeerList()
        self._soup = None
        self._cached_response = None
        self._url = kwargs.get('url', None)
        self._brewery_name = kwargs.get('brewery', None)

    # read_page(): This will actually read in the web page without making
    #              any adjustments, just the raw data encoded UTF-8
    def read_page(self, in_session:requests.sessions = None) -> bool:
        assert(self._url is not None)
        if not self._mocked:
            if in_session is not None:
                session = in_session
            else:
                session = requests.Session()
            rsp = session.get(self._url)
            assert(rsp is not None)
            rsp.encoding = 'utf-8'
            rsp_text = rsp.text
            if in_session is not None:
                session.close()
        else:
            filename = self._brewery_name.replace(' ', '') + '.html'
            cwd = os.getcwd()
            fp = open('../beerlister/tests/data/' + filename, mode='r', encoding='utf8')
            assert(fp is not None)
            rsp_text = fp.read()
            fp.close()

        self._soup = bs.BeautifulSoup(rsp_text, "html.parser")
        self._cached_response = rsp_text
        return self._soup is not None

    def add_beer(self, beer: Beer) -> None:
        self._beer_list.append(beer)

    def get_beerlist(self) -> BeerList:
        return self._beer_list

    # ssml_taplist: make our internal list of beers into an SSML
    #               formatted output
    def ssml_taplist(self) -> str:
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

