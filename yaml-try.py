__author__ = 'Mike Carifio <mike@carif.io>'


import os
import sys
import logging
import yaml
import urllib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()




class Database(yaml.YAMLObject):

    def __init__(self, database=None):
        self.read_write = os.environ.get("MYSQL_READ_WRITE") or database.get('read_write') or 'mysql://carif:pass@localhost'
        self.read_only = os.environ.get("MYSQL_READ_ONLY") or database.get('read_only') or 'mysql://carif:pass@localhost' or self.read_write


    def throw(self, exception):
        raise exception

    def get_read_write(self):
        return self.read_write

    def get_read_only(self):
        return self.read_only







class Configuration(yaml.YAMLObject):

    def __init__(self, production=None, development=None):
        self.production = os.environ.get('PRODUCTION') or production or Database(dict(read_write='mysql://db.host.com/database'))
        self.development = os.environ.get('DEVELOPMENT') or development or self.production


    def __repr__(self, *args, **kwargs):
         return "%s(production=%r, development=%r)" % (
             self.__class__.__name__, self.production, self.development)




# hack

def make_constructor(cls):
    def constructor(loader, node) :
        fields = loader.construct_mapping(node)
        return cls(**fields)
    return constructor

for cls in [Configuration, Database]:
    tag = '!' + cls.__name__
    yaml.add_constructor(tag, make_constructor(cls))



if '__main__' == __name__:
    logger.debug('start')
    # os.environ['PRODUCTION'] = 'foo'
    config = yaml.load("""
    !Configuration
    production:
        !Database
        database:
            read_write: mysql://username@password:host/database
            read_only: mysql://username@password:host/database
    development:
        !Database
        database:
            read_write: mysql://username@password:host:999/database
            #read_only: mysql://username@password:host:999/database

    """)

    print(config)

