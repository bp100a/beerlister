# -*- coding: utf-8 -*-
""" The Taplist for Breweries! """
# pylint: disable-msg=R0911, W0401
from controllers import brewerylist # for clarity
from models.breweries import *

SKILL_NAME = "TapList"
HELP_MESSAGE = "You can ask what is on tap at brewery name, " + \
               "or you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Taplist skill can't help you with that. " + \
                   "It can help you discover what beers are on tap " + \
                   "at select breweries in North Jersey"
FALLBACK_REPROMPT = 'What can I help you with?'

# --------------- App entry point -----------------


def lambda_handler(event, context):

    """  App entry point  """
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

    # process the intents

    if intent_name == "GetTapListIntent":
        return get_taplist_response(request['intent'])
    elif intent_name == 'ListBreweries':
        return list_of_breweries_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()

    return get_help_response()


def list_of_breweries_response():
    """Return a list of breweries that we support"""
    list_of_breweries = brewerylist.BREWERY_PAGES.ssml_brewery_list()
    return response(speech_response(list_of_breweries, True))


def get_taplist_response(intent: dict):
    """ return the taplist  """

    brewery_name = intent['slots']['brewery']['value']
    bobj, brewery_id = brewerylist.BREWERY_PAGES.find_brewery(brewery_name=brewery_name)

    # if we couldn't find the brewery, respond with a the list of breweries we know
    if brewery_id is None or bobj is None:
        return list_of_breweries_response()

    if 'mocked' in intent:
        bobj.mocking = intent['mocked']
    bobj.fetch_taplist(brewery=brewery_id)
    beer_string = bobj.ssml_taplist()
    speech_output = beer_string
    return response(speech_response_ssml(speech_output, True))


def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message, speech_message, False))


def get_launch_response():

    """ get and return the help string  """

    return response(HELP_MESSAGE)


def get_stop_response():

    """ end the session, user wants to quit """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))


def get_fallback_response():

    """ end the session, user wants to quit """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))


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


def dialog_response(endsession):

    """  create a simple json response with card """

    return {
        'version': '1.0',
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }


def speech_response_with_card(title, output, cardcontent, endsession):

    """  create a simple json response with card """

    return {
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardcontent
        },
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }


def response_ssml_text_and_prompt(output, endsession, reprompt_text):

    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }


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
