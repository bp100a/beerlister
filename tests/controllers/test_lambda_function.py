from unittest import TestCase
import os
import json
import lambda_function
from tests.setupmocking import TestwithMocking
from models import setuplogging


class TestAWSlambda(TestwithMocking):

    @staticmethod
    def data_dir() -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def get_taplist_intent(self, brewery):
        fn = self.data_dir() + 'GetTapListIntent_' + brewery.replace(' ', '') + '.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        event['request']['intent']['mocked'] = True
        response = lambda_function.lambda_handler(event=event, context=None)
        assert response is not None
        assert response['response']['shouldEndSession']

        # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
        fn = self.data_dir() + brewery.replace(' ', '') + '.SSML'
        fp = open(fn, mode='r', encoding='utf8')
        tst_data = '<speak>' + fp.read() + '</speak>'
        fp.close()
        if tst_data != response['response']['outputSpeech']['ssml']:
            assert False  # anything different, raise hell!

    def test_getTwinElephant(self):
        self.get_taplist_intent("Twin Elephant")

    def test_getBeerMenus(self):
        self.get_taplist_intent("Rinn Duin")

    def test_getUntapped(self):
        self.get_taplist_intent("Alementary")

    def test_getDigitalPour(self):
        self.get_taplist_intent(("Village Idiot"))

    def test_list_breweries_intent(self):
        """Test we can get a list of breweries using an Alexa intent from file"""
        fn = self.data_dir() + 'ListBreweries' + '.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        event['request']['intent']['mocked'] = True
        response = lambda_function.lambda_handler(event=event, context=None)
        assert response is not None
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == "Here are the breweries I know: Rinn Duin, " \
                                                               "Departed Soles, Twin Elephant, Fort Nonsense, " \
                                                               "Alementary, Man Skirt, Demented, Village Idiot, " \
                                                               "Jersey Girl, Angry Erik, and Trap Rock"

    def test_bogus_brewery(self):
        """Test that we get back the brewery list for an unknown brewery"""
        fn = self.data_dir() + 'GetTapListIntent_BogusBrewery.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        event['request']['intent']['mocked'] = True
        response = lambda_function.lambda_handler(event=event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Here are the breweries I know:')
        assert response['response']['shouldEndSession']

    def test_open_skill(self):
        fn = self.data_dir() + 'OpenTapList.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        response = lambda_function.lambda_handler(event=event['payload']['content']['invocationRequest']['body'], context=None)
        assert response is not None
        assert not response['response']['shouldEndSession']

    def test_session_state(self):

        # create our launch request
        launch_event = {"request" : {"type": "LaunchRequest"}, "session" : {"new": True} }
        response = lambda_function.lambda_handler(event=launch_event, context=None)
        assert not response['response']['shouldEndSession']

        # Session is open, now ask for a list of breweries
        list_breweries_event = {"request" : {"type": "IntentRequest", "intent": {"name": "ListBreweries", "mocked": True}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=list_breweries_event, context=None)
        assert response['response']['shouldEndSession']

    def test_fallback_response(self):
        get_fallback = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.FallbackIntent", "mocked": True}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_fallback, context=None)
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.FALLBACK_MESSAGE

    def test_cancel_response(self):
        get_cancel = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.CancelIntent", "mocked": True}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_cancel, context=None)
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.STOP_MESSAGE

    def test_stop_response(self):
        get_stop = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.StopIntent", "mocked": True}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_stop, context=None)
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.STOP_MESSAGE

    def test_help_response(self):
        get_help = {"request" : {"type": "IntentRequest",\
                                 "intent": {"name": "AMAZON.HelpIntent", "mocked": True}}, "session" : {"new": False}}
        response = lambda_function.lambda_handler(event=get_help, context=None)
        assert not response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.HELP_MESSAGE

    def test_unknown_intent_response(self):
        get_unknown = {"request" : {"type": "IntentRequest", "intent":\
                                    {"name": "JerseyBeers.UNKNOWN_INTENT", "mocked": True}},\
                       "session": {"new": False}}
        response = lambda_function.lambda_handler(event=get_unknown, context=None)
        assert not response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.HELP_MESSAGE

    def test_new_session(self):
        event_new_session = {"session": {"new": False}, "request" : {"type" : "Bogus"} }
        response = lambda_function.lambda_handler(event=event_new_session, context=None)
        assert response is None

    def test_end_session(self):
        event_end_session = {"session": {"new": False}, "request" : {"type": "SessionEndRequest"}}
        response = lambda_function.lambda_handler(event=event_end_session, context=None)
        assert response is None

    def test_set_home_brewery(self):
        """Test that we get back the brewery list for an unknown brewery"""
        fn = self.data_dir() + 'SetHomeBreweryIntent_RinnDuin.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        event['request']['intent']['mocked'] = True
        response = lambda_function.lambda_handler(event=event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Your home brewery has been set to')
        assert response['response']['shouldEndSession']

    def test_set_home_brewery_logging(self):
        set_home_event = {
            "request": {"type": "IntentRequest", "intent": {"name": "SetHomeBrewery", "mocked": True,\
                                                            "slots": {"brewery": {"value": "bogus"}}}},\
            "session": {"new": False, "user": {"userId": "bogus_user_id"}}}

        response = lambda_function.lambda_handler(event=set_home_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Sorry, I cannot set')
        assert response['response']['shouldEndSession']
        assert "brewery not found" in setuplogging.MOCK_LOG

    def test_get_tap_list_logging(self):
        get_tap_list_event = {
            "request": {"type": "IntentRequest", "intent": {"name": "GetTapListIntent", "mocked": True,\
                                                            "slots": {"brewery": {"value": "bogus"}}}},\
            "session": {"new": False, "user": {"userId": "bogus_user_id"}}}

        response = lambda_function.lambda_handler(event=get_tap_list_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Here are the breweries I know:')
        assert response['response']['shouldEndSession']
        assert "GetTapList, brewery not found" in setuplogging.MOCK_LOG

    def test_set_bad_home_brewery(self):
        """Test that we get back the brewery list for an unknown brewery"""
        fn = self.data_dir() + 'SetHomeBreweryIntent_RinnDuin.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        event['request']['intent']['mocked'] = True
        event['request']['intent']['slots']['brewery']['value'] = 'bogus brewing'

        response = lambda_function.lambda_handler(event=event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Sorry, I cannot set')
        assert response['response']['shouldEndSession']

    def test_bad_home_brewery_taplist(self):
        """try to set a bad brewery and get proper error response"""
        home_taplist_event = {"request" : {"type": "IntentRequest", "intent": {"name": "GetHomeTapList", "mocked": True}},\
                              "session" : {"new": False, "user": {"userId": "bogus_user_id"} } }
        response = lambda_function.lambda_handler(event=home_taplist_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Sorry, no home brewery has been set')
        assert response['response']['shouldEndSession']

    def test_home_brewery_taplist(self):
        """retrieve a home brewery tap list"""
        # first set the home brewery
        set_home_event = {"request" : {"type": "IntentRequest",\
                                       "intent": {"name": "SetHomeBrewery",
                                                  "mocked": True,
                                                  "slots" : {"brewery":{"value":"Twin Elephant"}}}},\
                          "session" : {"new": False, "user": {"userId": "valid_user_id"} } }
        response = lambda_function.lambda_handler(event=set_home_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['text'].startswith('Your home brewery has been set to')
        assert response['response']['shouldEndSession']

        home_taplist_event = {"request" : {"type": "IntentRequest",\
                                           "intent": {"name": "GetHomeTapList", "mocked": True}},\
                              "session" : {"new": False, "user": {"userId": "valid_user_id"} } }
        response = lambda_function.lambda_handler(event=home_taplist_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['ssml'].startswith('<speak>on tap at')
        assert response['response']['shouldEndSession']

    def test_set_home_brewery_no_slot(self):
        """retrieve fail setting the home brewery, ommit the slot"""
        # first set the home brewery
        set_home_event = {"request" : {"type": "IntentRequest",\
                                       "intent": {"name": "SetHomeBrewery",
                                                  "mocked": True}},\
                          "session" : {"new": False, "user": {"userId": "valid_user_id"} } }
        response = lambda_function.lambda_handler(event=set_home_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['type'] == 'PlainText'
        assert lambda_function.ERROR_NO_BREWERY in response['response']['outputSpeech']['text']
        assert response['response']['shouldEndSession']

    def test_get_home_brewery(self):
        """Test that we can set a home brewery and get it back"""
        set_home_event = {"request" : {"type": "IntentRequest",\
                                       "intent": {"name": "SetHomeBrewery",
                                                  "mocked": True,
                                                  "slots" : {"brewery":{"value":"Village Idiot"}}}},\
                          "session" : {"new": False, "user": {"userId": "valid_user_id"} } }

        response = lambda_function.lambda_handler(event=set_home_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['type'] == 'PlainText'
        assert response['response']['outputSpeech']['text'].startswith('Your home brewery has been set to')
        assert response['response']['shouldEndSession']

        # now read it back
        get_home_event = {"request" : {"type": "IntentRequest",\
                                       "intent": {"name": "GetHomeBrewery", "mocked": True}},\
                          "session" : {"new": False, "user": {"userId": "valid_user_id"} } }
        response = lambda_function.lambda_handler(event=get_home_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['type'] == 'PlainText'
        assert 'Village Idiot' in response['response']['outputSpeech']['text']
        assert response['response']['shouldEndSession']

    def test_get_home_brewery_none(self):
        """Test that when no home brewery has been set, we tell user"""
        # read a home brewery before we have set it
        get_home_event = {"request" : {"type": "IntentRequest",\
                                       "intent": {"name": "GetHomeBrewery", "mocked": True}},\
                          "session" : {"new": False, "user": {"userId": "valid_user_id"}}}
        response = lambda_function.lambda_handler(event=get_home_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['type'] == 'PlainText'
        assert 'Sorry, no home brewery' in response['response']['outputSpeech']['text']
        assert response['response']['shouldEndSession']

    def test_empty_brewery(self):
        """Test that we get back the brewery list for an unknown brewery"""
        empty_brewery_event = {"request": {"type": "IntentRequest",
                                           "intent": {"name": "GetTapListIntent",
                                                      "mocked": True,
                                                      "slots": {"brewery": {"value":""}}}},\
                              "session": {"new": False,
                                          "user": {"userId": "bogus_user_id"}}}
        response = lambda_function.lambda_handler(event=empty_brewery_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['type'] == 'PlainText'
        assert response['response']['outputSpeech']['text'].startswith('Here are the breweries I know:')
        assert response['response']['shouldEndSession']

    def test_get_taplist_no_slot(self):
        """Test that we get back the brewery list for an unknown brewery"""
        empty_brewery_event = {"request": {"type": "IntentRequest",
                                           "intent": {"name": "GetTapListIntent",
                                                      "mocked": True}},\
                              "session": {"new": False,
                                          "user": {"userId": "bogus_user_id"}}}
        response = lambda_function.lambda_handler(event=empty_brewery_event, context=None)
        assert response is not None
        assert response['response']['outputSpeech']['type'] == 'PlainText'
        assert lambda_function.ERROR_NO_BREWERY in response['response']['outputSpeech']['text']
        assert response['response']['shouldEndSession']

