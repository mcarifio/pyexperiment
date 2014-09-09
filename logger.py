# PAZIEN CONFIDENTIAL
#
# NOTICE:  All information contained herein is, and remains
#  the property of Pazien, Inc.
# 
#  Copyright (c) 2014 Pazien, Inc.

"""
module docstring for logger
"""

import os
import sys
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import logging

logging.basicConfig()
logger = logging.getRootLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)

if '__main__' == __name__:
    logger.info('start')
    # start here

    logger.info('exit with status %d', 0)
