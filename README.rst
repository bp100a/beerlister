[bp100a] Jersey Beers
=========================

.. contents:: Topics

.. image:: https://codecov.io/gh/bp100a/beerlister/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bp100a/beerlister

Overview
--------

Read a tap list from a brewery's website and parse it into something that can be read off by an Alexa Skill.

Currently read the following formats:

* UnTappd
    * Man Skirt
    * Alementary
    * Fort Nonsense
* Digital Pour
    * Village Idiot
* Beer Menus
    * Rinn Duin
* Custom scraped
    * Twin Elephant Brewing
    * Jersey Girl
    * Departed Soles
    * Angry Erik (10/9/2018)
    * Trap Rock

On the list
-----------
See issues

How it works
------------
You can ask the following:

"ask Jersey Beers what breweries do you know?"
"ask Jersey Beers what is on tap at {brewery name}?"
"ask Jersey Beers to set my home brewery to {brewery name}"
"ask Jersey Beers to get my home taplist"

I accept the obvious aliases for a brewery name e.g. "Alementary", "Alementary Brewery" and "Alementary Brewing", as well as "elementary". The brewery list read back will use the "shortest" name specified for the brewery. I've incorporated logging of mispronounced brewery names, so over time things should get better.

There's been a lot of testing and deployment incorporated into the codebase (not passwords!)
I'm using CircleCI to both build & deploy. Deployment uses lambda versions & alias with the following flow:

1) Build job
    * runs unit tests (+90 tests, all mocked in about 4 secs!)
    * runs PyLint (pretty darn clean)
2) Deploy job
    * run if no errors during build
    * deploys to arn:STAGE
    * runs integration tests (.json -> lambda function)
    * deploys to arn:PROD if integration tests succeed

Running integration tests catches dumb-ass errors like missing import statements that don't show up during build.

Had to change name to "Jersey Beers" since Alexa/Amazon doesn't allow a single word invocation name (unless it's a brand). Also fixed up session state management and added tests to validate.

If you have a favorite brewery you want included, send me a message!

Regards,

Harry
