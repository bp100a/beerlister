"""This is where we stash our brewery objects so they are all
in one place. Each brewery page needs to add itself to the global
list created at the end of this file."""
from typing import Tuple
import models.breweries.beerlist
import models.cloudredis


class BreweryLister:
    """This is our controller for the brewery list"""
    brewery_page_list: list[models.breweries.beerlist.BreweryPage] = []

    def add_home_brewery(self, brewery_name: str, user_id: str) -> bool:
        """set the specified brewery as the home brewery, return True if successful"""
        # check to see if the brewery exists
        brewery_page, brewery_id = self.find_brewery(brewery_name)
        if brewery_page is None or brewery_id is None:
            return False

        # set this as the new home brewery for this user
        models.cloudredis.REDIS_SERVER.set(models.cloudredis.home_key(user_id), brewery_id)
        return True

    @staticmethod
    def get_home_brewery(user_id: str) -> str:
        """return the home brewery if specified, otherwise 'None' """
        home_key = models.cloudredis.home_key(user_id)
        if not models.cloudredis.REDIS_SERVER.exists(home_key): # if key doesn't exist
            return ''

        return models.cloudredis.REDIS_SERVER.get(home_key)

    def add_brewery_page(self, brewery_page: models.breweries.beerlist.BreweryPage) -> None:
        """Adds a brewery page to the list we are managing"""
        self.brewery_page_list.append(brewery_page)

    def find_brewery(self, brewery_name) -> tuple[models.breweries.beerlist.BreweryPage | None, str]:
        """finds a brewery page in the list we are managing"""
        # look for the specified brewery in our list of breweries we know about
        for brewery_page in self.brewery_page_list:
            brewery_id = brewery_page.brewery_by_alias(brewery_name)
            if brewery_id is not None:
                return brewery_page, brewery_id

        return None, ''

    def list_of_breweries(self):
        """retrieve a list of all breweries by short name"""
        all_breweries = []
        for brewery_page in self.brewery_page_list:
            brewery_short_name = brewery_page.short_name()
            all_breweries.extend(brewery_short_name)

        # now we have a complete list of breweries
        return all_breweries

    def ssml_brewery_list(self):
        """create the SSML to speak the list of breweries we know about"""
        list_of_breweries = self.list_of_breweries()
        resp = 'Here are the breweries I know: '
        for i in range(len(list_of_breweries)): # pylint: disable=C0200

            if i == len(list_of_breweries) - 1:
                resp = resp + 'and ' + list_of_breweries[i]
            else:
                resp = resp + list_of_breweries[i] + ', '

        return resp


# initialize a "global" so all brewery pages can add themselves to this list
BREWERY_PAGES = BreweryLister()
