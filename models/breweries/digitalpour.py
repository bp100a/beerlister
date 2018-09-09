import bs4 as bs
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist

BREWERY_INFO = {"Village Idiot": ['556fbbe55e002c0d44d5bd22', 1]}


class DigitalPourPage(BreweryPage):
    """fetch the taplists we know about hosted by Digital Pour"""

    def __init__(self, *args, **kwargs):
        BreweryPage.__init__(self, *args, **kwargs)

        # initialize aliases
        self._alias = {"Village Idiot" : ["Village Idiot Brewery", "Village Idiot Brewing"]}

    def fetch_taplist(self, *args, **kwargs) -> None:
        """fetch the taplist and scrape out the beer list"""
        if kwargs.get('brewery') is not None:
            brewery = kwargs['brewery']

        # construct our URL
        loc_theme = BREWERY_INFO[brewery]
        url = "http://fbpage.digitalpour.com/?companyID={0}&locationID={1}".format(loc_theme[0], loc_theme[1])
        BreweryPage.fetch_taplist(self, url=url, **kwargs)
        assert self._url is not None
        self.read_page() # read the page
        assert self._cached_response is not None
        assert self._soup is not None
        start_string = '<body>'
        start_pos = self._cached_response.find(start_string)
        end_string = '</body>'
        end_pos = self._cached_response.find(end_string)
        html_menu = self._cached_response[start_pos:end_pos+len(end_string)]
        assert end_pos is not -1
        self._soup = bs.BeautifulSoup(html_menu, "html.parser")
        assert self._soup is not None

        beer_div_list = self._soup.find_all("div", {"class": "beverageInfo"})
        assert(beer_div_list is not None)
        for beer in beer_div_list:
            if beer.contents[1].text:
                beer_name = beer.contents[3].text
                beer_style = beer.contents[7].text
                beer_abv = beer.contents[11].text.strip()
                beer_ibu = beer.contents[13].text.split(' ')[0]
                self.add_beer(Beer(name=beer_name, style=beer_style, abv=beer_abv, ibu=beer_ibu, desc=None))


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(DigitalPourPage())
