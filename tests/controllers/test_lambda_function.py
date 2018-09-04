from unittest import TestCase
import lambda_function

class TestAWSlambda(TestCase):

    def test_intent(self):
        event = { 'session' : {'new' : True},
                  'request' : {'type':'IntentRequest',
                               'intent':{'name': 'GetTapListIntent'}} }
        response = lambda_function.lambda_handler(event=event, context=None)
        assert(response['version'] == '1.0')
        assert(response['response']['outputSpeech'] is not None)
        assert(False) # fail until we test output returned for veracity