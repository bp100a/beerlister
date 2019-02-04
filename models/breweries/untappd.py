"""scrape breweries using UnTapped for their tap list"""
import bs4 as bs
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist

BREWERY_INFO = {"Fort Nonsense": [14504, 53940], "Alementary": [1192, 955],
                "Man Skirt": [1576, 2092], "Demented": [1591, 2137],
                "Pinelands": [8415,29881],
                "Untied": [21632, 82353]}


class UnTappdPage(BreweryPage):
    """breweries hosted by UnTapped"""

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Fort Nonsense": ["Fort Nonsense Brewing",
                                         "Fort Nonsense Brewery",
                                         "fortnite incense"],
                       "Alementary": ["Alementary Brewing",
                                      "Alementary Brewery",
                                      "elementary",
                                      "elementary brewing",
                                      "elementary brewery"],
                       "Man Skirt": ["Man Skirt Brewing",
                                     "Man Skirt Brewery",
                                     "man's skirt",
                                     "mansker"],
                       "Demented": ["Demented Brewing",
                                    "Demented Brewery"],
                       "Pinelands": ["Pinelands Brewing",
                                     "Pinelands Brewery"],
                       "Untied": ["Untied Brewing",
                                  "Untied Brewery",
                                  "United", "United Brewing", "United Brewery",
                                  "Untied Browing",
                                  "Untied Brewing Company"]}

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
                            if i_c.contents[1].contents[1].attrs['class'][0] == 'abv':
                                beer_abv = i_c.contents[1].contents[1].text.split('%')[0] + '%'
                            if 'ibu-hideable' in i_c.contents[3].attrs['class']:
                                beer_ibu = i_c.contents[3].contents[1].text.split(' ')[0]
                        elif 'item-description' in i_c.attrs['class']:
                            i_beer_desc = i_c.text.split('\\n')
                            beer_desc = i_beer_desc[2].strip()

        self.add_beer(Beer(name=beer_name, style=beer_style, abv=beer_abv,
                           ibu=beer_ibu, desc=beer_desc))

    @staticmethod
    def untied_filter(tag) -> bool:
        if (tag.has_attr('class') and "menu-info" in tag.attrs['class']) or \
                (tag.has_attr('class') and "item-title-color" in tag.attrs['class']):
            return True

        return False

    def untied_parser(self, html_menu: str):
        """special parser for Untied Brewing's page"""

        # for now just list the core beers
        beer_span_list = self._soup.find_all("tr", {"class": "item-title-color"})
        div_list = self._soup.find_all("div", {"class": "item-description"})
        all_list = self._soup.find_all(UnTappdPage.untied_filter)
        assert beer_span_list is not None
        beer_idx = 0
        menu_index = 0
        for beer_entry in all_list:
            if "menu-info" in beer_entry.attrs["class"]:
                menu_index += 1
                if menu_index > 2:  # Core & Premium menus
                    break
            else:
                if len(beer_entry.contents[3].contents) > 2:
                    try:
                        beer_name = beer_entry.contents[1].contents[1].text.split('.')[1]
                        beer_style = beer_entry.contents[3].contents[1].text.strip('\\n ')
                        beer_abv = beer_entry.contents[5].text.strip('\\n ')
                        beer_ibu = beer_entry.contents[7].text.strip('\\n ')
                        beer_desc = div_list[beer_idx].contents[3].text
                        self.add_beer(Beer(name=beer_name, style=beer_style, abv=beer_abv,
                                           ibu=beer_ibu, desc=beer_desc))
                        beer_idx += 1
                    except IndexError as ie:
                        break

        return

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch and scrape the tap list page for UnTappd"""
        brewery = kwargs.get('brewery')
        assert brewery is not None

        # construct our URL
        url = "https://business.untappd.com/locations/{0}/themes/{1}/js" \
            .format(BREWERY_INFO[brewery][0], BREWERY_INFO[brewery][1])

        # perform any pre-fetch initialization of base class
        BreweryPage.fetch_taplist(self, url=url, **kwargs)
        assert self._url is not None
        is_cached = self.read_page(brewery) # read the page
        if is_cached:
            return True

        assert self._cached_response is not None

        start_string = 'container.innerHTML = "'
        start_pos = self._cached_response.find(start_string)
        end_pos = self._cached_response.find('(function (){')
        end_pos2 = self._cached_response.rfind('"', 0, end_pos)
        html_menu = self._cached_response[start_pos + len(start_string):end_pos2]
        html_menu = html_menu.replace('\\"', '"')
        html_menu = html_menu.replace('/\n', '\n')
        html_menu = html_menu.replace('\\/', '/')

        self._soup = bs.BeautifulSoup(html_menu, "html.parser")
        assert self._soup is not None
        beer_div_list = self._soup.find_all("div", {"class": "beer"})
        assert beer_div_list is not None
        if len(beer_div_list) == 0:
            self.untied_parser(html_menu)
        else:
            section_name_list = self._soup.find_all("div", {"class" : "section-name"})
            draft_section = section_name_list[0].text
            for beer in beer_div_list:
                section_name = beer.find_previous("div", "section-name")
                if section_name.text != draft_section:
                    break
                assert beer is not None
                self.parse_inner_content(beer)

        return False # not from the cache

# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(UnTappdPage())
