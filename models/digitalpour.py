
from models.beerlist import BreweryPage
from models.beerlist import Beer
import string
import bs4 as bs
import html.parser

brewery_info = {"Village Idiot" : ['556fbbe55e002c0d44d5bd22', 1]}

# http://fbpage.digitalpour.com/?companyID=556fbbe55e002c0d44d5bd22&locationID=1

class DigitalPourPage(BreweryPage):
    # digital pour hosted brewery menus

    def __init__(self, *args, **kwargs) -> None:
        if kwargs.get('brewery') is not None:
            brewery = kwargs['brewery']
        else:
            brewery = 'Fort Nonsense Brewing'

        # construct our URL
        loc_theme = brewery_info[brewery]
        url = "http://fbpage.digitalpour.com/?companyID={0}&locationID={1}".format(loc_theme[0], loc_theme[1])
        BreweryPage.__init__(self, url=url, brewery=brewery)
        assert(self._url is not None)
        self.read() # read the page
        assert(self._cached_response is not None)
        assert(self._soup is not None)
        start_string = '<body>'
        start_pos = self._cached_response.text.find(start_string)
        end_string = '</body>'
        end_pos = self._cached_response.text.find(end_string)
        html_menu = self._cached_response.text[start_pos:end_pos+len(end_string)]
        assert(end_pos is not -1)
        self._soup = bs.BeautifulSoup(html_menu, "html.parser")
        assert(self._soup is not None)

        beer_div_list = self._soup.find_all("div", {"class": "beverageInfo"})
        assert(beer_div_list is not None)
        for beer in beer_div_list:
            if beer.contents[1].text:
                beer_name = beer.contents[3].text
                beer_style = beer.contents[7].text
                beer_abv = beer.contents[11].text.strip()
                beer_ibu = beer.contents[13].text.split(' ')[0]
                self.add_beer(Beer(name=beer_name, style=beer_style, abv=beer_abv, ibu=beer_ibu, desc=None))
