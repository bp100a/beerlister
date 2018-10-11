"""brewery page to web scrape departed soles website for tap list"""
import re
from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class AngryErikPage(BreweryPage):
    """scrape website of Departed Soles Brewing, Jersey City"""
    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {"Angry Erik": ["Angry Erik Brewing",
                                      "Angry Erik Brewery",
                                      "Angry Eric",
                                      "Angry Eric Brewing",
                                      "Angry Eric Brewery"]}

    def parse_beer_text(self, beer_string: str):
        """
           'Ravol - An American Amber, 6.8% ABV'
           'Ravol w/ Pumpkin Pie Herbal Blend- An American Amber, 6.8% ABV'
           '2018 Hop Harvest IPA: Get Naked - Wet-Hopped IPA, 7.5% ABV'
           'Viva Verde! - Jalepeno IPA, 7.5% ABV - Hoppy Heide #2'
           'Bourbon Barrel-Aged Vanagandr - Belgian-style Brown Ale, 7.0% ABV'

        :param beer_string:
        :return:
        """
        beer_string = beer_string.replace('\u00f8', 'o')
        beer_string = beer_string.replace('\u00A1', '')
        # beer_string = beer_string.replace('\u2013', '-')
        beer_name = ''
        beer_style = ''
        beer_abv = ""
        parts = re.split('-|,|\u2013', beer_string)
        if len(parts) == 3:
            beer_name = parts[0].strip()
            beer_style = parts[1].replace('An ', '').strip()
            beer_abv = parts[2].split('%')[0].strip() + '%'
        else:
            for part in parts:
                if "% ABV" in part:
                    beer_abv = part.split('%')[0].strip() + '%'

            # okay the first '-' or \u2013 is inclusive to the name
            parts = beer_string.split(',')
            name_and_style = parts[0]
            more_parts = name_and_style.split('\u2013')
            beer_name = more_parts[0].strip()
            beer_style = more_parts[1].strip()

        if beer_name and beer_style:
            self.add_beer(Beer(name=beer_name,
                               style=beer_style,
                               abv=beer_abv,
                               hops=None))

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch the taplist page for Angry Erik and parse it"""
        BreweryPage.fetch_taplist(self, url="http://www.angryerik.com/services.html", **kwargs)
        assert self._url is not None
        is_cached = self.read_page(brewery=list(self._alias.keys())[0])  # read the page
        if is_cached:
            return True

        span_list = self._soup.find_all("span")
        for span in span_list:
            if '**' in span.text:
                return False
            contents = span.contents
            if not contents:
                continue
            if hasattr(contents[0], 'name') and contents[0].name == 'u':
                beer_name = contents[0].text
                if beer_name:
                    self.parse_beer_text(beer_name)


        return False # not from cache


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(AngryErikPage())
