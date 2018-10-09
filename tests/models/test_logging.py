from unittest import TestCase
from models import setuplogging


class MockAWSLogging():

    @staticmethod
    def info(message: str) -> None:
        assert message is not None


class TestLogging(TestCase):

    def test_setup_logging_mocked(self):
        setuplogging.AWS_LOGGER = None
        setuplogging.LOGGING_HANDLER = None

        setuplogging.initialize_logging(mocking=True)
        assert setuplogging.AWS_LOGGER is None
        assert setuplogging.LOGGING_HANDLER == setuplogging.mock_logging_handler

    def test_setup_logging_prod(self):
        setuplogging.AWS_LOGGER = None
        setuplogging.LOGGING_HANDLER = None

        setuplogging.initialize_logging(mocking=False)
        assert setuplogging.AWS_LOGGER is not None
        assert setuplogging.LOGGING_HANDLER == setuplogging.prod_logging_handler

    def test_logging_to_prod(self):
        setuplogging.AWS_LOGGER = None
        setuplogging.LOGGING_HANDLER = None

        setuplogging.initialize_logging(mocking=False)
        setuplogging.AWS_LOGGER = MockAWSLogging()

        event = {'bogus event': 'data'}
        context = {'bogus context': 'bogus'}
        setuplogging.LOGGING_HANDLER(event, context)
