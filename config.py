"""
config module, one per executable
"""

import os
import sys
import yaml
import attrdict


class Database(yaml.YAMLObject):

    def __init__(self, read_write=None, read_only=None):
        self.read_write = os.environ.get("MYSQL_READ_WRITE") or read_write or 'mysql://carif:pass@localhost'
        self.read_only = os.environ.get("MYSQL_READ_ONLY") or read_only or 'mysql://carif:pass@localhost' or self.read_write

    def make(self, a: attrdict)->Database:
        self.__init__(read_write=a.database.read_write)

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

    def make(self, attr):


    def __repr__(self, *args, **kwargs):
         return "%s(production=%r, development=%r)" % (
             self.__class__.__name__, self.production, self.development)



def make_constructor(cls):
    def constructor(loader, node) :
        fields = loader.construct_mapping(node)
        return cls(**fields)
    return constructor

for cls in [Configuration, Database]:
    tag = '!' + __name__ +'.' + cls.__name__
    yaml.add_constructor(tag, make_constructor(cls))

