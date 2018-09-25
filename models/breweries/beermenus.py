"""Read the tap list for breweries hosted by BeerMenus"""
import bs4 as bs
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist

BREWERY_INFO = {"Rinn Duin" : [17853]}


class BeerMenusPage(BreweryPage):
    """BeerMenus hosted taplists"""

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Rinn Duin" : ["Rinn Duin Brewing", "Rinn Duin Brewery"]}

    def fetch_taplist(self, **kwargs) -> None:
        """fetch the taplist for this specific beer management software"""
        if kwargs.get('brewery') is not None:
            brewery = kwargs['brewery']

        # construct our URL
        url = "https://beermenus.com/menu_widgets/{0}".format(BREWERY_INFO[brewery][0])
        BreweryPage.fetch_taplist(self, url=url, **kwargs)
        self.read_page(brewery=brewery) # read the page

        assert self._cached_response is not None
        start_string = 'widgetDiv.innerHTML = \'\\n'
        start_pos = self._cached_response.find(start_string)
        end_pos = self._cached_response.rfind(';\n}')
        html_menu = self._cached_response[start_pos+len(start_string):end_pos-1]
        html_menu = html_menu.replace('\\"', '"')
        html_menu = html_menu.replace('\\n', '\n')
        html_menu = html_menu.replace('\\/', '/')
        assert end_pos is not -1
        self._soup = bs.BeautifulSoup(html_menu, "html.parser")
        assert self._soup is not None
        taplist_table = self._soup.find('table', attrs={'class': 'on_tap-section'})
        table_body = taplist_table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(row.contents) > 3:
                self.add_beer(Beer(name=cols[0].text.strip().split('\n')[1], style=None,
                                   abv=cols[1].text.strip() + '%', ibu=None, desc=None))


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(BeerMenusPage())
