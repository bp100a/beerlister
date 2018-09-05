# -*- coding: utf-8 -*-
from controllers import brewerylist # for clarity
from models.breweries import *

""" simple fact sample app """

SKILL_NAME = "TapList"
GET_TAPLIST_MESSAGE = "Here's your beer list: "
HELP_MESSAGE = "You can say what is ontap at brewery name, or you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Taplist skill can't help you with that.  It can help you discover what beers are on tap at Twin Elephant Brewing. What can I help you with?"
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


# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """
    intent_name = request['intent']['name']

    # process the intents

    if intent_name == "GetTapListIntent":
        return get_taplist_response(request['intent'])
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        return get_help_response()


def get_taplist_response(intent : dict):

    """ return the taplist  """
    bobj, brewery_id = brewerylist.brewery_pages.find_brewery(brewery_name=intent['slots']['brewery'])
    if 'mocked' in intent:
        bobj._mocked = intent['mocked']
    bobj.fetch_taplist(brewery=brewery_id)
    beer_string = bobj.ssml_taplist()
    speechOutput = beer_string
    return response(speech_response_ssml(speechOutput, True))

def get_help_response():

    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message, speech_message, False))

def get_launch_response():

    """ get and return the help string  """

    return get_taplist_response()

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