"""
config module, one per executable
"""

import os
import sys
import yaml
import attrdict


class Database(yaml.YAMLObject):
    """
    Database represents a pair of database connection strings in SQLAlchemy format, i.e. 'mysql://username:password@hostname/database'.
    read_write is a read/write database, read_only is its read_only variant.
    """

    def __init__(self, read_write=None, read_only=None):
        """
        Usage: db = config.Database(read_write='mysql://username:password@hostname/database', read_only='mysql://username:password@hostname/database')
        Can be overridden by environment variables MYSQL_READ_WRITE and MYSQL_READ_ONLY
        :param read_write:
        :param read_only:
        :return:
        """
        self._initialize(read_write, read_only)

    def _initialize(self, read_write, read_only):
        """
        Internal method to initialize an instance's contents. You can get here multiple ways: directly via __init__ or indirectly via populate().
        :param read_write:
        :param read_only:
        :return:
        """
        self._read_write = os.environ.get('MYSQL_READ_WRITE') or read_write or 'mysql://username:password@hostname/database' or self.throw(ValueError("expecting a read_write connect string"))
        self._read_only = os.environ.get('MYSQL_READ_ONLY') or read_only or self.read_write

    def populate(self, a: attrdict):
        """
        Usage: config.Dictionary().populate(a:attrict.AttrDict). Populates a Dictionary from an attribute dictionary (with the right attributes).
        :param a:
        :return:
        """
        self._initialize(a.read_write, a.read_only)
        return self

    def __repr__(self, *args, **kwargs):
        return "%s(read_write=%r, read_only=%r)" % (
            self.__class__.__name__, self.read_write, self.read_only)

    def throw(self, e):
        """
        Raise is a statement, throw is an expression.
        :param e:
        :return:
        """
        raise e

    # getters
    @property
    def read_write(self):
        return self._read_write

    @property
    def read_only(self):
        return self._read_only







class Configuration(yaml.YAMLObject):
    """
    Configuration represents an application configuration. It can be parsed directly in pyyaml with the appropriate configuration directives,
    e.g. !config.Configuration or it can be constructed from an attrdict.AttrDict. See conf_yaml.py for example usage.
    """

    def __init__(self, production=None, development=None):
        """
        Usage: c = config.Configuration(production=config.Database(...))
        :param production:
        :param development:
        :return:
        """
        self._initialize(production, development)

    def _initialize(self, production, development):
        """
        Internal method to initialize an instance's contents. Call constructors get here.
        :param production:
        :param development:
        :return:
        """
        self._production = os.environ.get('PRODUCTION') or production or Database(read_write='mysql://user:pass@db.host.com/database')
        self._development = os.environ.get('DEVELOPMENT') or development or self.production

    def populate(self, a: attrdict):
        """
        Usage: c = config.Configuration().populate(a:attr.AttrDict). Populates a Configuration from an attribute dictionary (with right attributes).
        :param a:
        :return:
        """
        self._initialize(a.production, a.development)
        return self


    # pyyaml says we need this.
    def __repr__(self, *args, **kwargs):
         return "%s(production=%r, development=%r)" % (
             self.__class__.__name__, self.production, self.development)


    # getters
    @property
    def production(self):
        return self._production

    @property
    def development(self):
        return self._development




# Magic hackery to register tags in the format '!config.Configuration' etc with each class's constructor.
# Experimented my way to nirvana.
def make_constructor(cls):
    def constructor(loader, node) :
        fields = loader.construct_mapping(node)
        return cls(**fields)
    return constructor

for cls in [Configuration, Database]:
    tag = '!' + __name__ +'.' + cls.__name__
    yaml.add_constructor(tag, make_constructor(cls))

