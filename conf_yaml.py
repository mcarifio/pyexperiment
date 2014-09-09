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

def name_from(pathname):
    if pathname:
        return os.path.join(os.path.dirname(pathname), os.path.basename(os.path.splitext(pathname)[0]), '.conf.yaml')
    else:
        raise ValueError("Expecting pathname, received None.")

def read_conf_yaml(pathname = None, called_from = None):
    yaml_file = pathname or name_from(called_from)
    with open(yaml_file) as fstream:
        return attrdict.AttrDict(yaml.load(fstream))

if '__main__' == __name__:
    logger.info('start')
    # start here

    try:
        pathname = 'example.conf.yaml'
        config = read_conf_yaml(pathname=pathname)
    except FileNotFoundError as e:
        logger.exception(e)


    print(config.production.database.rw)

    logger.info('exit with status %d', 0)
