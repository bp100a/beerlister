
from models.beerlist import BreweryPage
from models.beerlist import Beer
import string
import bs4 as bs
import html.parser

brewery_info = {"Rinn Duin Brewing" : [17853]}

# https://www.beermenus.com/menu_widgets/17853

class BeerMenusPage(BreweryPage):
    # digital pour hosted brewery menus

    def __init__(self, *args, **kwargs) -> None:
        if kwargs.get('brewery') is not None:
            brewery = kwargs['brewery']
        else:
            brewery = 'Rinn Duin Brewing'

        # construct our URL
        loc_theme = brewery_info[brewery]
        url = "https://beermenus.com/menu_widgets/{0}".format(loc_theme[0])
        BreweryPage.__init__(self, url=url, brewery=brewery)
        assert(self._url is not None)
        self.read() # read the page
        assert(self._cached_response is not None)
        assert(self._soup is not None)
        start_string = 'widgetDiv.innerHTML = \'\\n'
        start_pos = self._cached_response.text.find(start_string)
        end_string = ';\n}'
        end_pos = self._cached_response.text.rfind(end_string)
        html_menu = self._cached_response.text[start_pos+len(start_string):end_pos-1]
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


