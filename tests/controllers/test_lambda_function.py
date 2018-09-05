from unittest import TestCase
import lambda_function
import os
import json

class TestAWSlambda(TestCase):

    @staticmethod
    def data_dir() -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('/tests')[0]
        path = root + '/tests/data/'
        return path

    def test_gettaplistintent(self):
        breweries = ["Twin Elephant", "Rinn Duin Brewing", "Alementary Brewing"]

        for brewery in breweries:
            fn = self.data_dir() + 'GetTapListIntent_' + brewery.replace(' ', '') + '.json'
            fp = open(fn, mode='r', encoding='utf8')
            json_intent = fp.read()
            fp.close()
            event = json.loads(json_intent)
            event['request']['intent']['mocked'] = True
            response = lambda_function.lambda_handler(event=event, context=None)
            assert(response is not None)

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn =  self.data_dir() + brewery.replace(' ', '') + '.SSML'
            fp = open(fn,  mode='r', encoding='utf8')
            tst_data = '<speak>' + fp.read() + '</speak>'
            fp.close()
            if (tst_data != response['response']['outputSpeech']['ssml']):
                assert(False)# anything different, raise hell!

    def test_listbreweries_intent(self):

            fn = self.data_dir() + 'ListBreweries' + '.json'
            fp = open(fn, mode='r', encoding='utf8')
            json_intent = fp.read()
            fp.close()
            event = json.loads(json_intent)
            event['request']['intent']['mocked'] = True
            response = lambda_function.lambda_handler(event=event, context=None)
            assert(response is not None)

    def test_bogusbrewery(self):

        fn = self.data_dir() + 'GetTapListIntent_BogusBrewery.json'
        fp = open(fn, mode='r', encoding='utf8')
        json_intent = fp.read()
        fp.close()
        event = json.loads(json_intent)
        event['request']['intent']['mocked'] = True
        response = lambda_function.lambda_handler(event=event, context=None)
        assert(response is not None)
        assert(response['response']['outputSpeech']['text'].startswith('Here are the breweries I know:'))
