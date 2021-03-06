"""classes to manage our beers and list of beers.
Also the brewery page is here, this is the base object
for all brewery website scraping and is overridden
for brewery specific needs"""
import re
import os
import time
import requests
import bs4 as bs
from models import cloudredis


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
        if self.name:
            self.name = self.name.strip()
        if self.style:
            self.style = self.style.strip()
        if self.abv:
            self.abv = self.abv.strip()
            if '%' not in self.abv:
                self.abv += '%'

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
        self.mocking = kwargs.get('mocked', False)
        self._url = kwargs.get('url', None)

    @property
    def mocking(self):
        """our property setter for the internal mocked state"""
        return self._mocked

    @mocking.setter
    def mocking(self, mocked: bool):
        """so we can hid protected member"""
        self._mocked = mocked

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
            short_list.append(brewery)

        return short_list

    def fetch_taplist(self, **kwargs) -> bool:
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
    def read_page(self, brewery: str, in_session: requests.sessions = None) -> bool:
        """Read the brewery page
        returns True if fresh cache entry found"""
        assert self._url is not None
        if not self.mocking:
            if in_session is not None:
                session = in_session
            else:
                session = requests.Session()

            try:
                session.verify = False
                rsp = session.get(self._url)
            except Exception: # pylint: disable=W0703
                return False

            rsp.encoding = 'utf-8'
            rsp_text = rsp.text
            if in_session is not None:
                session.close()
        else:
            filename = self._brewery_name.replace(' ', '') + '.HTML'
            file_pointer = open(BreweryPage.testdata_dir() + filename, mode='r', encoding='utf8')
            assert file_pointer is not None
            rsp_text = file_pointer.read()
            file_pointer.close()

        self._cached_response = rsp_text # save for later
        if not BreweryPage.is_cached(brewery, rsp_text):
            self._soup = bs.BeautifulSoup(rsp_text, "html.parser")
            return False # not cached

        return True # cached

    @staticmethod
    def is_cached(brewery, rsp_text) -> bool:
        """Check to see if this brewery's webpage has already
        been read and we can save a lot of work
        =True, then we have a cache of this response"""
        assert brewery is not None and rsp_text is not None
        assert cloudredis.REDIS_SERVER is not None

        # check if there's a valid cache entry
        return cloudredis.md5_exists(brewery, rsp_text)

    def add_beer(self, beer: Beer) -> None:
        """add a beer to our private list"""
        self._beer_list.append(beer)

    @staticmethod
    def spell_out_strings(string_with_ipa: str) -> str:
        """Fix up IPA strings so it's spelled out by Alexa"""
        if 'DDH' in string_with_ipa:
            string_with_ipa = string_with_ipa.\
                replace('DDH', 'double dry hopped')

        if 'IBU' in string_with_ipa:
            string_with_ipa = string_with_ipa.\
                replace('IBU', '<say-as interpret-as="spell-out">IBU</say-as>')

        if 'ABV' in string_with_ipa:
            string_with_ipa = string_with_ipa.\
                replace('ABV', '<say-as interpret-as="spell-out">ABV</say-as>')

        if 'NEIPA' in string_with_ipa: # pylint:disable=R1705
            return string_with_ipa.\
                replace('NEIPA', 'New England <say-as interpret-as="spell-out">IPA</say-as>')
        elif 'DIPA' in string_with_ipa:
            return string_with_ipa.\
                replace('DIPA', 'double <say-as interpret-as="spell-out">IPA</say-as>')
        elif 'IRA' in string_with_ipa:
            return string_with_ipa.\
                replace('IRA', '<say-as interpret-as="spell-out">IRA</say-as>')
        elif 'APA' in string_with_ipa:
            return string_with_ipa.\
                replace('APA', '<say-as interpret-as="spell-out">APA</say-as>')
        return string_with_ipa.\
            replace('IPA', '<say-as interpret-as="spell-out">IPA</say-as>')

    # ssml_taplist: make our internal list of beers into an SSML
    #               formatted output
    def ssml_taplist(self) -> str:
        """Create the SSML that drives speech for the list of beers"""
        # first things first - check the cache!
        beer_str = cloudredis.ssml_from_cache(self._brewery_name)
        if beer_str is not None:
            return beer_str

        # create a string for the tap list we have
        beer_str = 'on tap at ' + self._brewery_name + '<break strength="strong"/>'
        if not self._beer_list:
            return beer_str + "no beers listed"

        # okay, we have some beers, so iterate through them
        vowels = "aeiou"
        for beer in self._beer_list:
            if 'IT' in beer.name:
                beer_name = beer.name.replace('IT ', '<sub alias="it"> IT </sub>')
            else:
                beer_name = beer.name
            beer_str += ' ' + self.spell_out_strings(beer_name)
            if beer.style is not None:
                beer_style = self.spell_out_strings(beer.style)
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

        beer_str = beer_str.replace(' & ', ' and ')
        beer_str = beer_str.replace('&', ' and ')

        # okay, let's cache this
        cloudredis.cache_ssml(self._brewery_name, self._cached_response, beer_str, int(time.time()))
        return beer_str
