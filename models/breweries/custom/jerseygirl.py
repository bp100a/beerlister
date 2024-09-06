""" Brewery Page to scrape Jersey Girl's web site for a taplist"""

from models.breweries.beerlist import BreweryPage
from models.breweries.beerlist import Beer
from controllers import brewerylist


class JerseyGirlPage(BreweryPage):
    """Twin Elephant Brewing Company, Chatham NJ
    main page has list of beers on tap:

    "beer-name"
    "beer-style" (description is next
    "ABV"
    "OG"
    "COLOR:"
    "MALT:"
    "HOPS:"
    "YEAST:"
    "Misc:"
    """

    def __init__(self, **kwargs):
        BreweryPage.__init__(self, **kwargs)

        # initialize aliases
        self._alias = {
            "Jersey Girl": ["jerseygirl", "Jersey Girl Brewing", "Jersey Girl Brewery"]
        }

    @staticmethod
    def parse_content(abv_and_style: str):
        """parse the ABV & style from jersey girl strings:
        1) 'ABV- 10.0% Belgian Tripel'
        2) '7.5% ABV - West Coast Style IPA'
        3) 'ABV: 6.2% - French Saison',
        4) 'ABV - 6.5% - New England Style IPA'
        5) 'ABV 4.5% - Traditional, German-style Pilsner'
        """
        parts = abv_and_style.split(" ")
        style = ""
        abv = None
        for idx in range(0, len(parts)):  # pylint: disable=C0200
            if "%" in parts[idx]:
                abv = parts[idx]
                continue
            if "ABV" in parts[idx] or parts[idx] == "-" or parts[idx] == "\N{En Dash}":
                continue
            style += parts[idx] + " "
        style = style.replace("NE-", "New England ")
        if abv is None or not style:
            return None, None

        return abv.strip(" "), style.strip(" ")

    def find_beers(self, content: list) -> None:
        """okay, from this list, find the beer name, ABV & style."""

        # first the beer name
        for beer_idx in range(0, len(content)):  # pylint: disable=C0200
            if hasattr(content[beer_idx], "name") and content[beer_idx].name == "u":
                # okay we have the beer name
                beer_name = content[beer_idx].text
                # now find the ABV
                abv_idx = 0
                for abv_idx in range(beer_idx + 1, len(content)):
                    if "ABV" in content[abv_idx]:
                        beer_abv, beer_style = JerseyGirlPage.parse_content(
                            content[abv_idx]
                        )
                        if (
                            beer_abv is None or beer_style is None
                        ):  # end of what's on tap
                            return
                        if beer_abv != "0.0%":
                            self.add_beer(
                                Beer(
                                    name=beer_name,
                                    style=beer_style,
                                    abv=beer_abv,
                                    hops=None,
                                )
                            )
                            break
                abv_idx += 1  # out of loop, advance next search by 1
                if abv_idx == len(content):
                    return
                beer_idx = abv_idx

    def fetch_taplist(self, **kwargs) -> bool:
        """fetch taplist for Jersey Girl, directly scraping their site and parsing"""

        span_list = kwargs.get("mockedlist", None)  # testing injection
        # perform any pre-fetch initialization of base class
        BreweryPage.fetch_taplist(
            self, url="http://www.jerseygirlbrewing.com/beers.html", **kwargs
        )

        if span_list is None:
            is_cached = self.read_page(
                brewery=list(self._alias.keys())[0]
            )  # read the page
            if is_cached:
                return True
            span_list = self._soup.find_all("span")

        idx = 0
        taplist_start_found = False
        for idx in range(0, len(span_list)):  # pylint: disable=C0200
            span = span_list[idx]
            taplist_start_found = "On Tap in the Sample Room" in span.text
            if taplist_start_found:
                break

        if not taplist_start_found:
            return False

        # okay we found the Tap List span, now look for beers
        for beer_span_idx in range(idx + 1, len(span_list)):
            beer_span = span_list[beer_span_idx]
            if (
                hasattr(beer_span, "contents")
                and isinstance(beer_span.contents, list)
                and beer_span.contents
            ):
                beer_span_contents = beer_span.contents[0]
                if (
                    hasattr(beer_span_contents, "contents")
                    and isinstance(beer_span_contents.contents, list)
                    and len(beer_span_contents.contents) > 2
                ):
                    self.find_beers(beer_span_contents.contents)
                    return False

        return False  # not from cache


# add this to the list of breweries
brewerylist.BREWERY_PAGES.add_brewery_page(JerseyGirlPage())
