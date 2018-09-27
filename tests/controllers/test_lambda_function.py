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

    def test_gettaplistintent(self):
        """Test that we can get brewery response for a pre-canned intent object"""
        breweries = ["Twin Elephant", "Rinn Duin", "Alementary", "Village Idiot"]

        for brewery in breweries:
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
                assert False# anything different, raise hell!

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
