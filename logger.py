"""
Configure the root logger and get an instance.
"""
import logging
logging.basicConfig()
root_logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
root_logger.setLevel(logging.WARNING)
