# -*- coding: utf-8 -*-
""" Jersey Beers Alexa Skill! Returns the tap list for your favorite brewery """
# pylint: disable-msg=R0911, W0401, R1705, W0613
from controllers import brewerylist # for clarity
from models.breweries import * # instantiate all our brewery page scrapers
from models.breweries.custom import *  # instantiate the custom scraped breweries
from models import cloudredis, setuplogging


SKILL_NAME = "Jersey Beers"
HELP_MESSAGE = "You can ask what is on tap at select breweries by name, " + \
               "or you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Jersey Beers skill can't help you with that. " + \
                   "It can help you discover what beers are on tap " + \
                   "at select breweries in North Jersey"
FALLBACK_REPROMPT = 'What can I help you with?'
HOME_BREWERY_SET = 'Your home brewery has been set to {0}'
CANNOT_SET_HOME = 'Sorry, I cannot set {0} as your home brewery'
NO_HOME_BREWERY_SET = 'Sorry, no home brewery has been set. You can set your home brewery' + \
                      'by saying ask Jersey Beers to set my home brewery to a brewery'
CURRENT_HOME_BREWERY = "Your current home brewery is {0}"
ERROR_NO_BREWERY = "I'm sorry, you must specify a brewery"
ERROR_BREWERY_PAGE = "Sorry, I'm having problems reading that breweries tap list. /" \
                     "I have notified the proper authorities"


def lambda_handler(event, context):

    """  App entry point  """
    setuplogging.initialize_logging(mocking=False) # make sure logging is setup
    setuplogging.LOGGING_HANDLER('EVENT{}'.format(event)) # log the event

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

    return None

# --------------- Response handlers -----------------


def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']

    # initialize our redis server if needed
    if cloudredis.REDIS_SERVER is None:
        cloudredis.initialize_cloud_redis(injected_server=None)

    # process the intents

    if intent_name == "GetTapListIntent":
        return get_taplist_response(request['intent'])
    elif intent_name == 'ListBreweries':
        return list_of_breweries_response()
    elif intent_name == 'SetHomeBrewery':
        return set_home_brewery(request, session)
    elif intent_name == 'GetHomeTapList':
        return get_home_brewery_taplist(request, session)
    elif intent_name == 'GetHomeBrewery':
        return get_home_brewery(request, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()

    return get_help_response()


def get_home_brewery_taplist(request: dict, session: dict):
    """get the taplist for our home brewery"""
    aws_user_id = session['user']['userId']
    brewery = brewerylist.BREWERY_PAGES.get_home_brewery(user_id=aws_user_id)
    if not brewery: # didn't find a home
        return response(speech_response(NO_HOME_BREWERY_SET, True))

    # okay, we have a home brewery, so lets get the tap list
    mocked = False
    if 'mocked' in request['intent']:
        mocked = request['intent']['mocked']
    taplist_intent = {"slots":{"brewery":{"value": brewery.decode('utf-8')}}, "mocked": mocked}
    return get_taplist_response(taplist_intent)


def set_home_brewery(request: dict, session: dict):
    """set the home brewery for the user"""

    try:
        brewery = request['intent']['slots']['brewery']['value']
        aws_user_id = session['user']['userId']
        success = brewerylist.BREWERY_PAGES.add_home_brewery(brewery_name=brewery,
                                                             user_id=aws_user_id)
        if success:
            return response(speech_response(HOME_BREWERY_SET.format(brewery), True))

        # some problem, tell the user. TBD validate brewery & other things,
        # perhaps ask for clarification
        setuplogging.LOGGING_HANDLER("SetHomeBrewery, brewery not found:\"{0}\"".format(brewery))
        return response(speech_response(CANNOT_SET_HOME.format(brewery), True))
    except KeyError:
        return response(speech_response(ERROR_NO_BREWERY, True))


def get_home_brewery(request: dict, session: dict):
    """get the home brewery for the user"""

    aws_user_id = session['user']['userId']
    brewery = brewerylist.BREWERY_PAGES.get_home_brewery(user_id=aws_user_id)
    if not brewery: # didn't find a home
        return response(speech_response(NO_HOME_BREWERY_SET, True))

    # some problem, tell the user. TBD validate brewery & other things,
    # perhaps ask for clarification
    return response(speech_response(CURRENT_HOME_BREWERY.format(brewery), True))


def list_of_breweries_response():
    """Return a list of breweries that we support"""
    list_of_breweries = brewerylist.BREWERY_PAGES.ssml_brewery_list()
    return response(speech_response(list_of_breweries, True))


def get_taplist_response(intent: dict):
    """ return the taplist  """
    try:
        brewery_name = intent['slots']['brewery']['value']
        bobj, brewery_id = brewerylist.BREWERY_PAGES.find_brewery(brewery_name=brewery_name)

        # if we couldn't find the brewery, respond with a the list of breweries we know
        if brewery_id is None or bobj is None:
            setuplogging.LOGGING_HANDLER("GetTapList, brewery not found: \"{0}\""\
                                         .format(brewery_name))
            return list_of_breweries_response()

        if 'mocked' in intent:
            bobj.mocking = intent['mocked']
        bobj.fetch_taplist(brewery=brewery_id)
        beer_string = bobj.ssml_taplist()
        return response(speech_response_ssml(beer_string, True))
    except KeyError:
        return response(speech_response(ERROR_NO_BREWERY, True))
    except Exception:
        setuplogging.LOGGING_HANDLER("PAGELOAD failure!! brewery \"{0}\""\
                                     .format(brewery_name))
        return response(speech_response(ERROR_BREWERY_PAGE, True))


def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message, speech_message, False))


def get_launch_response():

    """ get and return the help string  """

    return response(speech_response(HELP_MESSAGE, False))


def get_stop_response():

    """ end the session, user wants to quit """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))


def get_fallback_response():

    """ end the session, user wants to quit """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, True))


def on_session_started():

    """" called when the session starts  """

    #print("on_session_started")


def on_session_ended():

    """ called on session ends """

    #print("on_session_ended")


def on_launch(request):

    """ called on Launch, we reply with a launch message  """
    return get_launch_response()


# --------------- Speech response handlers -----------------

def speech_response_ssml(output, endsession):

    """  create a simple json response  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + output + '</speak>'
        },
        'shouldEndSession': endsession
    }


def speech_response(output, endsession):

    """  create a simple json response  """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }


# def dialog_response(endsession):
#
#     """  create a simple json response with card """
#
#     return {
#         'version': '1.0',
#         'response':{
#             'directives': [
#                 {
#                     'type': 'Dialog.Delegate'
#                 }
#             ],
#             'shouldEndSession': endsession
#         }
#     }


# def speech_response_with_card(title, output, cardcontent, endsession):
#
#     """  create a simple json response with card """
#
#     return {
#         'card': {
#             'type': 'Simple',
#             'title': title,
#             'content': cardcontent
#         },
#         'outputSpeech': {
#             'type': 'PlainText',
#             'text': output
#         },
#         'shouldEndSession': endsession
#     }


# def response_ssml_text_and_prompt(output, endsession, reprompt_text):
#
#     """ create a Ssml response with prompt  """
#
#     return {
#         'outputSpeech': {
#             'type': 'SSML',
#             'ssml': "<speak>" +output +"</speak>"
#         },
#         'reprompt': {
#             'outputSpeech': {
#                 'type': 'SSML',
#                 'ssml': "<speak>" +reprompt_text +"</speak>"
#             }
#         },
#         'shouldEndSession': endsession
#     }


def speech_response_prompt(output, reprompt_text, endsession):

    """ create a simple json response with a prompt """


    return {

        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },

        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }


def response(speech_message) -> dict:

    """ create a simple json response  """

    return {
        'version': '1.0',
        'response': speech_message
    }
