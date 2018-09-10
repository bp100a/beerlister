"""classes to manage our beers and list of beers.
Also the brewery page is here, this is the base object
for all brewery website scraping and is overridden
for brewery specific needs"""
import re
import os
import requests
import bs4 as bs


class Beer():
    """the essence of a beer. A list of beers is the 'tap list' for brewery"""
    name = None
    style = None
    abv = None
    hops = []
    ibu = None
    desc = None

    def __init__(self, **kwargs):
        """our generic 'beer'. A small amount of parsing"""
        self.name = kwargs.get('name')
        self.style = kwargs.get('style')
        self.abv = kwargs.get('abv')
        if kwargs.get('ibu') is not None:
            self.ibu = kwargs.get('ibu')
        if kwargs.get('desc') is not None:
            self.desc = kwargs.get('desc')
        if kwargs.get('hops') is not None:
            self.hops = re.split('& |, ', kwargs.get('hops'))

        if self.style is not None:
            self.style = self.style.replace(u'\xf6', 'o') # fix umla in Kolsch

    def has_hops(self) -> bool:
        """determine if hops have been specified for this beer"""
        return self.hops is not None and len(self.hops) > 0


class BeerList(list):
    """"our beer list manager - the tap list for a brewery"""
    def append(self, beer: Beer) -> None:
        """simple list mananger to hide the particulars"""
        list.append(self, beer)


class BreweryPage():
    """responsible for fetching the brewery page. Overidden as needed"""
    _url = None
    _brewery_name = None
    _soup = None
    _cached_response = None
    _beer_list = None
    _mocked = False
    _include_hops = True
    _alias = [] # defined by derived classes in __init__() method

    def __init__(self, **kwargs) -> None:
        """initialize our brewery page. Determine if testing or what attributes we have"""
        self._include_hops = kwargs.get('hops')
        self._mocked = kwargs.get('mocked', False)
        self._url = kwargs.get('url', None)

    def brewery_by_alias(self, brewery_name) -> str:
        """For this brewery page manager, find the brewrey by alias"""
        # search the alias list for what brewery
        for brewery in self._alias:
            if brewery_name.lower() == brewery.lower():
                return brewery
            for brewery_alias in self._alias[brewery]:
                if brewery_name.lower() == brewery_alias.lower():
                    return brewery
        return None

    def short_name(self) -> list:
        """this is the short name of the brewery we use when speaking"""
        short_list = list()
        for brewery in self._alias:
            shortest_name = brewery
            for alias in self._alias[brewery]:
                if len(alias) < len(shortest_name):
                    shortest_name = alias
            short_list.append(shortest_name)

        return short_list

    def fetch_taplist(self, **kwargs):
        """retrieve the taplist for the brewery"""
        self._beer_list = BeerList()
        self._soup = None
        self._cached_response = None
        self._url = kwargs.get('url', None)
        self._brewery_name = kwargs.get('brewery', None)

    @staticmethod
    def testdata_dir() -> str:
        """return the directory where test data lives"""
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    # read_page(): This will actually read in the web page without making
    #              any adjustments, just the raw data encoded UTF-8
    def read_page(self, in_session: requests.sessions = None) -> bool:
        """Read the brewery page"""
        assert self._url is not None
        if not self._mocked:
            if in_session is not None:
                session = in_session
            else:
                session = requests.Session()
            rsp = session.get(self._url)
            assert rsp is not None
            rsp.encoding = 'utf-8'
            rsp_text = rsp.text
            if in_session is not None:
                session.close()
        else:
            filename = self._brewery_name.replace(' ', '') + '.html'
            file_pointer = open(BreweryPage.testdata_dir() + filename, mode='r', encoding='utf8')
            assert file_pointer is not None
            rsp_text = file_pointer.read()
            file_pointer.close()

        self._soup = bs.BeautifulSoup(rsp_text, "html.parser")
        self._cached_response = rsp_text
        return self._soup is not None

    def add_beer(self, beer: Beer) -> None:
        """add a beer to our private list"""
        self._beer_list.append(beer)

    def get_beerlist(self) -> BeerList:
        """retrieve our private beer list"""
        return self._beer_list

    # ssml_taplist: make our internal list of beers into an SSML
    #               formatted output
    def ssml_taplist(self) -> str:
        """Create the SSML that drives speech for the list of beers"""
        # create a string for the tap list we have
        assert self._beer_list is not None
        assert self._brewery_name is not None
        beer_str = 'on tap at ' + self._brewery_name + '<break strength="strong"/>'
        if not self._beer_list:
            return beer_str + "no beers listed"

        # okay, we have some beers, so iterate through them
        vowels = "aeiou"
        for beer in self._beer_list:
            beer_str += ' ' + beer.name.replace('IT', '<sub alias="it"> IT </sub>')

            if beer.style is not None:
                if 'DIPA' in beer.style:
                    beer_style = beer.style.replace('DIPA',
                                                    'double <say-as interpret-as="spell-out">IPA</say-as>')
                else:
                    beer_style = beer.style.replace('IPA',
                                                    '<say-as interpret-as="spell-out">IPA</say-as>')
                if beer.style[0].lower() in vowels:
                    beer_str += ", an " + beer_style
                else:
                    beer_str += ", a " + beer_style
            if beer.abv is not None:
                beer_str += " that is " + beer.abv + " alcohol"
            if beer.has_hops():
                beer_str += ", hopped with "
                if len(beer.hops) == 1:
                    beer_str += beer.hops[0]
                else:
                    beer_str += "{} and {}".format(", ".join(beer.hops[:-1]), beer.hops[-1])

            beer_str += "."

        return beer_str
