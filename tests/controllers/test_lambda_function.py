from unittest import TestCase
import os
import json
import lambda_function
from tests.setupfakeredis import TestwithFakeRedis

class TestAWSlambda(TestwithFakeRedis):

    @staticmethod
    def data_dir() -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def get_taplistintent(self, brewery):
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
        self.get_taplistintent("Twin Elephant")

    def test_getBeerMenus(self):
        self.get_taplistintent("Rinn Duin")

    def test_getUntapped(self):
        self.get_taplistintent("Alementary")

    def test_getDigitalPour(self):
        self.get_taplistintent(("Village Idiot"))

    def test_listbreweries_intent(self):
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
        assert response['response']['outputSpeech']['text'] == 'Here are the breweries I know: Rinn Duin, Twin Elephant, Fort Nonsense, Alementary, Angry Erik, Man Skirt, Demented, Village Idiot, and Jersey Girl'

    def test_bogusbrewery(self):
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

    def test_openskill(self):
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
        launchevent = {"request" : {"type": "LaunchRequest"}, "session" : {"new": True} }
        response = lambda_function.lambda_handler(event=launchevent, context=None)
        assert not response['response']['shouldEndSession']

        # Session is open, now ask for a list of breweries
        listbreweriesevent = {"request" : {"type": "IntentRequest", "intent": {"name": "ListBreweries"}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=listbreweriesevent, context=None)
        assert response['response']['shouldEndSession']

    def test_fallback_response(self):
        get_fallback = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.FallbackIntent"}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_fallback, context=None)
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.FALLBACK_MESSAGE

    def test_cancel_response(self):
        get_cancel = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.CancelIntent"}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_cancel, context=None)
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.STOP_MESSAGE

    def test_stop_response(self):
        get_stop = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.StopIntent"}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_stop, context=None)
        assert response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.STOP_MESSAGE

    def test_help_response(self):
        get_help = {"request" : {"type": "IntentRequest", "intent": {"name": "AMAZON.HelpIntent"}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_help, context=None)
        assert not response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.HELP_MESSAGE

    def test_unknown_intent_response(self):
        get_unknown = {"request" : {"type": "IntentRequest", "intent": {"name": "JerseyBeers.UNKNOWN_INTENT"}}, "session" : {"new": False} }
        response = lambda_function.lambda_handler(event=get_unknown, context=None)
        assert not response['response']['shouldEndSession']
        assert response['response']['outputSpeech']['text'] == lambda_function.HELP_MESSAGE

    def test_new_session(self):
        event_new_session = {"session": {"new": False}, "request" : {"type" : "Bogus"} }
        response = lambda_function.lambda_handler(event=event_new_session, context=None)
        assert response is None

    def test_end_session(self):
        event_end_session = {"session": {"new": False}, "request" : {"type" : "SessionEndRequest"} }
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
