"""Here's where we manage logging"""
import logging

LOGGING_HANDLER = None
AWS_LOGGER = None


def initialize_logging(mocking=True):
    """Determine if we use a real logger or our stub"""
    global AWS_LOGGER
    global LOGGING_HANDLER
    if LOGGING_HANDLER is not None:
        return

    if not mocking:
        AWS_LOGGER = logging.getLogger()
        AWS_LOGGER.setLevel(logging.INFO)
        LOGGING_HANDLER = prod_logging_handler
    else:
        LOGGING_HANDLER = mock_logging_handler


def prod_logging_handler(event, context):
    """where all things production go, logged to CloudWatch"""
    global AWS_LOGGER
    AWS_LOGGER.info('got event{}'.format(event))


def mock_logging_handler(event, context):
    """where all testing/debugging goes"""
    pass
