
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
import bs4 as bs
from controllers import brewerylist

BREWERY_INFO = {"Rinn Duin Brewing" : [17853]}

# https://www.beermenus.com/menu_widgets/17853

class BeerMenusPage(BreweryPage):
    # BeerMenus hosted brewery menus

    def __init__(self, *args, **kwargs):
        BreweryPage.__init__(self, *args, **kwargs)

        # initialize aliases
        self._alias = {"Rinn Duin Brewing" : ["Rinn Duin","Rinn Duin Brewery"]}

    def fetch_taplist(self, *args, **kwargs) -> None:
        if kwargs.get('brewery') is not None:
            brewery = kwargs['brewery']

        # construct our URL
        loc_theme = BREWERY_INFO[brewery]
        url = "https://beermenus.com/menu_widgets/{0}".format(loc_theme[0])
        BreweryPage.fetch_taplist(self, url=url, **kwargs)
        assert(self._url is not None)
        self.read_page() # read the page
        assert(self._cached_response is not None)
        assert(self._soup is not None)
        start_string = 'widgetDiv.innerHTML = \'\\n'
        start_pos = self._cached_response.find(start_string)
        end_string = ';\n}'
        end_pos = self._cached_response.rfind(end_string)
        html_menu = self._cached_response[start_pos+len(start_string):end_pos-1]
        html_menu = html_menu.replace('\\"', '"')
        html_menu = html_menu.replace('\\n', '\n')
        html_menu = html_menu.replace('\\/', '/')
        assert(end_pos is not -1)
        self._soup = bs.BeautifulSoup(html_menu, "html.parser")
        assert(self._soup is not None)
        ontap_list = self._soup.find_all("tbody", {"class": "on_tap"})
        taplist_table = self._soup.find('table', attrs={'class': 'on_tap-section'})
        table_body = taplist_table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(row.contents) > 3:
                beer_name = cols[0].text.strip().split('\n')[1]
                beer_abv = cols[1].text.strip() + '%'
                self.add_beer(Beer(name=beer_name, style=None, abv=beer_abv, ibu=None, desc=None))

# add this to the list of breweries
brewerylist.brewery_pages.add_brewery_page(BeerMenusPage())