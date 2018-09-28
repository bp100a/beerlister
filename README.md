# beerlister
.. contents:: Topics

.. image:: https://codecov.io/gh/bp100a/beerlister/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bp100a/beerlister
  
Read a tap list from a brewery's website and parse it into something that can be read off by an Alexa Skill.

Currently read the following formats:
- UnTappd (Man Skirt, Alementary, Fort Nonsense & Angry Erik)
- Digital Pour (Village Idiot)
- Beer Menus (Rinn Duin)
- ~~Departed Soles (Jersey City, NJ)~~ (taplists are not up to date)
- Twin Elephant Brewing (Chatham, NJ)

TBD:
- Jersey Girl Brewery

I'm from Jersey so I'm concentrating on Jersey Breweries. I use BeautifulSoup (awesome!) to parse the HTML I scrape from the brewery and create an internal list of beers. Not all breweries provide all the information, but when available we pull the name, style, abv, ibu and hops for each beer.

You can ask the following:

"ask Jersey Beers what breweries do you know?"
"ask Jersey Beers what is on tap at {brewery name}?"

I accept the obvious aliases for a brewery name e.g. "Alementary", "Alementary Brewery" and "Alementary Brewing". The brewery list read back will use the "shortest" name specified for the brewery.

There's been a lot of testing and deployment incorporated into the codebase (not passwords!)
I'm using CircleCI to both build & deploy. Deploy's happen if the build passes, which means all tests run clean and Pylint has no errors. Looking into ways to add a Pylint threshold (i.e. all modules must lint out to > 9, no more than xxx total warnings, etc.)

Had to change name to "Jersey Beers" since Alexa/Amazon doesn't allow a single word invocation name (unless it's a brand). Also fixed up session state management and added tests to validate.

Things I'd like to add:
   1) Read UnTappd REST API
      UnTappd has granted me access to their API, it would be nice to use it.
   2) More intelligent cache management
      right now just keeping cache for 1 hour, better if we look for changes (not all sites return any info in header)
   3) More breweries! Scraping takes time, but I'd like to add "strategic" breweries.
   4) Better "hearing"
      Alexa sucks interpreting free text. e.g. "Man Skirt" comes across as "mansker" a lot. I can account for this a wee bit
      by adding "aliases" to my brewery names, but that can get old and may eventually run into conflicts.
   5) Ability to set home brewery
      It would be cool if you could say "Alexa ask Jersey Beers what's on tap?" and not have to specify your favorite brewery.
   6) New beer notifications
      it'd be cool if we could notify the user if a brewery has changed their tap list
   
If you have a favorite brewery you want included, send me a message!

Regards,

Harry
