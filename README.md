# beerlister
Read a tap list from a brewery's website and parse it into something that can be read off by an Alexa Skill.

Currently read the following formats:
- UnTappd (Man Skirt, Alementary, Fort Nonsense & Angry Erik)
- Digital Pour (Village Idiot)
- Beer Menus (Rinn Duin)
- Departed Soles (Jersey City, NJ)
- Twin Elephant Brewing (Chatham, NJ)

TBD:
- Jersey Girl Brewery

I'm from Jersey so I'm concentrating on Jersey Breweries. I use BeautifulSoup (awesome!) to parse the HTML I scrape from the brewery and create an internal list of beers. Not all breweries provide all the information, but when available we pull the name, style, abv, ibu and hops for each beer.

You can ask the following:

"ask TapList what breweries do you know?"
"ask Taplist, what is on tap at {brewery name}?"

I accept the obvious aliases for a brewery name e.g. "Alementary", "Alementary Brewery" and "Alementary Brewing". The brewery list read back will use the "shortest" name specified for the brewery.

There's been a lot of testing and deployment incorporated into the codebase (note passwords!)

TBD:
- CACHEING! This is important as tap lists don't change often
- robustness. This code, while well tested, doesn't handle problems gracefully. If the pages scrape change their structure, we'll do very bad things.
- more breweries!


If you have a favorite brewery you want included, send me a message!

Regards,

Harry
