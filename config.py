"""
config module, one per executable
"""

import os
import sys
import yaml
import attrdict



def name_from(pathname, extension='.conf.yaml'):
    """Generate a yaml configuration pathname from a pathname. So '/some/path/foo.py' => '/some/path/foo.conf.yaml"""
    if pathname:
        return os.path.join(os.path.dirname(pathname), os.path.basename(os.path.splitext(pathname)[0]), extension)
    else:
        raise ValueError("Expecting pathname, received None.")

def attrdict_from_yaml_file(pathname=None, called_from=None):
    """
    Slurp an attrdict.AttrDict from a file pathname. For convenience, read_conf_yaml(called_from=__filename__) should work.
    """
    yaml_file = pathname or name_from(called_from)
    with open(yaml_file) as fstream:
        return yaml.load(fstream)

def attrdict_from_yaml_string(s):
    """Convenience for testing."""
    return yaml.load(s)


class DatabaseTBS(yaml.YAMLObject):
    """
    Database represents a pair of database connection strings in SQLAlchemy format, i.e. 'mysql://username:password@hostname/database'.
    read_write is a read/write database, read_only is its read_only variant.
    """

    def __init__(self, read_write=None, read_only=None, **kwargs):
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







class Configurations(yaml.YAMLObject):
    """
    Configuration represents an application configuration. It can be parsed directly in pyyaml with the appropriate configuration directives,
    e.g. !config.Configuration or it can be constructed from an attrdict.AttrDict. See conf_yaml.py for example usage.
    """

    def __init__(self, contents):
        """
        Usage: c = config.Configuration(production=config.Database(...))
        :param production:
        :param development:
        :return:
        """
        self._initialize(contents)

    def _initialize(self, contents):
        """
        Internal method to initialize an instance's contents. Call constructors get here.
        :param production:
        :param development:
        :return:
        """
        self.contents = attrdict.AttrDict(contents)
        for k,v in self.contents.items():
            override = os.environ.get(k.upper())
            if override:
                self.contents[k] = override
            elif isinstance(v, dict):
                self.contents[k] =  attrdict.AttrDict(v)
            self.__setattr__(k, self.contents[k])

    def select(self, item=None):
        if item:
            return self[item]
        else:
            return self.contents


    # Treat a Configuration as a dictionary like object.
    def __getitem__(self, item):
        """
        Usage: c = config.Configuration(...); c['production'] => Dictionary
        :param item:
        :type: str
        :return: database object with name item, relies of properties to get it right.
        :rtype: Database
        """
        return self.contents[item]

    def __iter__(self):
        """
        Usage: c['name'] => Database. Assumes all property names start with '_' (which is brittle).
        :return:
        """
        for k,v in self.contents.items():
            yield v
        raise StopIteration()

    # pyyaml says we need this.
    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__ + '(' + ','.join(['{}=%r'.format(k) for k in self.content.keys() ]) +')'


    # getters
    # @property
    # def production(self):
    #     return self._production
    #
    # @property
    # def development(self):
    #     return self._development




# Magic hackery to register tags in the format '!config.Configuration' etc with each class's constructor.
# Experimented my way to nirvana.
def make_constructor(cls):
    def constructor(loader, node) :
        fields = loader.construct_mapping(node)
        return cls(**fields)
    return constructor

for cls in [Configurations]: # Remove Database for now
    tag = '!' + __name__ +'.' + cls.__name__
    yaml.add_constructor(tag, make_constructor(cls))

