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
        title: "Production"
        read_write: "mysql://username@password:host/database1"
        read_only: "mysql://username@password:host/database1"

    development:
        !config.Database
        title: "Development"
        read_write: "mysql://username@password:host:999/database"
    """)

    print(config)

