import os
import sys
import logging
import yaml
import urllib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

import config


if '__main__' == __name__:
    logger.debug('start')
    # os.environ['PRODUCTION'] = 'foo'
    config = yaml.load("""
    !config.Configuration
    production:
        !config.Database
        { read_write: "mysql://username@password:host/database", read_only: "mysql://username@password:host/database" }
    development:
        !config.Database
        { read_write: "mysql://username@password:host:999/database "}
    """)

    print(config)

