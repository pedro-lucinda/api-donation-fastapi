"""
This configuration module sets up logging for the application. It configures
logging to output to stdout, a file, and the Logtail logging service.

Attributes
----------
formatter : logging.Formatter
    Defines the format of the log messages.
stream_handler : logging.StreamHandler
    Handles logging output to stdout.
file_handler : logging.FileHandler
    Handles logging output to a file named 'app.log'.
logs : LogtailHandler
    Sends log messages to the Logtail service using a provided token.

The logging level is set to INFO, meaning all INFO, WARNING, ERROR, and CRITICAL
messages will be logged.
"""

import logging
import sys

from logtail import LogtailHandler

from app.config.env_variables import LOGGER_TOKEN

# get logger
logger = logging.getLogger()

# create formatter
formatter = logging.Formatter(
    fmt='%(levelname)s - %(asctime)s - %(name)s - %(funcName)s -  %(filename)s - %(message)s'
)

# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
logs = LogtailHandler(source_token=LOGGER_TOKEN)

# set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers
logger.handlers = [stream_handler, file_handler, logs]

# set level
logger.setLevel(logging.INFO)
