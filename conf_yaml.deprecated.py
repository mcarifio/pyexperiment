#!/usr/bin/env python

"""
module docstring for conf_yaml
"""

import os
import sys
from logger import root_logger
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import yaml
import attrdict

import config


if '__main__' == __name__:
    logger.info('start')
    # start here

    try:
        pathname = 'example.conf.yaml'
        a = config.attrdict_from_yaml_file(pathname=pathname)
        c = config.Configurations(a)
    except FileNotFoundError as e:
        logger.exception(e)


    # use the stuff

    print(c.production.database.read_write)

    # the "top" level attributes in the Configuration are considered its "keys", i.e. 'production' and 'development'
    # TODO: pycharm completes these names?
    for k in c:
        print(k, c[k].database, c[k].database.read_write)

    # and finally
    env = os.environ.get("APP_ENV", "development")
    print(c[env].database.read_write)


    logger.info('exit with status %d', 0)
