from unittest import TestCase
import lambda_function
import os


class TestAWSlambda(TestCase):

    @staticmethod
    def data_dir() -> str:
        # return the test data directory from the current root
        cwd = os.getcwd().replace('\\', '/')
        root = cwd.split('tests')[0]
        path = root + 'tests/data/'
        return path

    def test_intent(self):
        breweries = ["Twin Elephant", "Alementary Brewing", "Angry Erik", "Rinn Duin Brewing", "Departed Soles", "Demented Brewing", "Fort Nonsense Brewing"]

        for brewery in breweries:
            event = { 'session' : {'new' : True},
                      'request' : {'type':'IntentRequest',
                                   'intent':{'name': 'GetTapListIntent', 'slots' : {'brewery' : brewery}, 'mocked':True}}}
            response = lambda_function.lambda_handler(event=event, context=None)
            assert(response['version'] == '1.0')
            assert(response['response']['outputSpeech'] is not None)

            # read our pre-canned response to compare with (../tests/data/<brewery>.SSML)
            fn =  self.data_dir() + brewery.replace(' ', '') + '.SSML'
            fp = open(fn,  mode='r', encoding='utf8')
            tst_data = '<speak>' + fp.read() + '</speak>'
            fp.close()
            if (tst_data != response['response']['outputSpeech']['ssml']):
                assert(False)# anything different, raise hell!
