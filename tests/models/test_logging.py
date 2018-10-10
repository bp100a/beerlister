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
        """In this test we do all the prod setup but we change
        out where PROD logs to and log to a locally defined function"""
        setuplogging.AWS_LOGGER = None
        setuplogging.LOGGING_HANDLER = None

        setuplogging.initialize_logging(mocking=False)
        setuplogging.AWS_LOGGER = MockAWSLogging()

        string_to_log = "log this string"
        setuplogging.LOGGING_HANDLER(string_to_log)

    def test_logging_to_mocked(self):
        """Our mocked log is just a string, so make sure we stash it in the right place"""
        setuplogging.AWS_LOGGER = None
        setuplogging.LOGGING_HANDLER = None

        setuplogging.initialize_logging(mocking=True)

        string_to_log = "log this string"
        setuplogging.LOGGING_HANDLER(string_to_log)
        assert string_to_log == setuplogging.MOCK_LOG
