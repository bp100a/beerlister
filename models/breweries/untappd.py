"""scrape breweries using UnTapped for their tap list"""
import bs4 as bs
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist

BREWERY_INFO = {"Fort Nonsense Brewing": [14504, 53940], "Alementary Brewing": [1192, 955],
                "Angry Erik": [11871, 43606], "Man Skirt Brewing": [1576, 2092],
                "Demented Brewing": [1591, 2137]}


class UnTappdPage(BreweryPage):
    """breweries hosted by UnTapped"""

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Fort Nonsense Brewing": ["Fort Nonsense", "Fort Nonsense Brewery"],
                       "Alementary Brewing": ["Alementary", "Alementary Brewery"],
                       "Angry Erik": ["Angry Erik Brewing", "Angry Erik Brewery"],
                       "Man Skirt Brewing": ["Man Skirt", "Man Skirt Brewery"],
                       "Demented Brewing": ["Demented", "Demented Brewery"]}

    def parse_inner_content(self, beer) -> None:
        """parse the content for beer information"""
        beer_name = None
        beer_style = None
        beer_ibu = None
        beer_abv = None
        beer_desc = None
        for content in beer:
            if hasattr(content, 'attrs') and 'class' in content.attrs and \
                    'beer-details' in content.attrs['class']:
                for i_c in content:
                    if hasattr(i_c, 'attrs') and 'class' in i_c.attrs:
                        if 'beer-name' in i_c.attrs['class']:
                            i_beer_name = i_c.text.split('\\n')
                            beer_name = i_c.contents[1].contents[2].replace('\\n', '').strip()
                            beer_style = i_beer_name[4].strip()
                        elif 'item-meta' in i_c.attrs['class']:
                            beer_abv = i_c.contents[1].contents[1].text.split('%')[0] + '%'
                            if 'ibu-hideable' in i_c.contents[3].attrs['class']:
                                beer_ibu = i_c.contents[3].contents[1].text.split(' ')[0]
                        elif 'item-description' in i_c.attrs['class']:
                            i_beer_desc = i_c.text.split('\\n')
                            beer_desc = i_beer_desc[2].strip()

        self.add_beer(Beer(name=beer_name, style=beer_style, abv=beer_abv,
                           ibu=beer_ibu, desc=beer_desc))

    def fetch_taplist(self, **kwargs) -> None:
        """fetch and scrape the tap list page for UnTappd"""
        brewery = kwargs.get('brewery')
        assert brewery is not None

        # construct our URL
        url = "https://business.untappd.com/locations/{0}/themes/{1}/js" \
            .format(BREWERY_INFO[brewery][0], BREWERY_INFO[brewery][1])

        # perform any pre-fetch initialization of base class
        BreweryPage.fetch_taplist(self, url=url, **kwargs)
        assert self._url is not None
        self.read_page() # read the page
        assert self._cached_response is not None
        assert self._soup is not None

        start_string = 'container.innerHTML = "'
        start_pos = self._cached_response.find(start_string)
        end_pos = self._cached_response.find('(function (){')
        end_pos2 = self._cached_response.rfind('"', 0, end_pos)
        html_menu = self._cached_response[start_pos + len(start_string):end_pos2]
        html_menu = html_menu.replace('\\"', '"')
        html_menu = html_menu.replace('/\n', '\n')
        html_menu = html_menu.replace('\\/', '/')
        if end_pos == -1:
            assert end_pos is not -1

        self._soup = bs.BeautifulSoup(html_menu, "html.parser")
        assert self._soup is not None
        beer_div_list = self._soup.find_all("div", {"class": "beer"})
        assert beer_div_list is not None
        section_name_list = self._soup.find_all("div", {"class" : "section-name"})
        draft_section = section_name_list[0].text
        for beer in beer_div_list:
            section_name = beer.find_previous("div", "section-name")
            if section_name.text != draft_section:
                break
            assert beer is not None
            self.parse_inner_content(beer)


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(UnTappdPage())
