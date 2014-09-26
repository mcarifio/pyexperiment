"""
try sqlalchemy
"""
import string

__author__ = 'Mike Carifio <mike@carif.io>'

import sys
import os
import logging
logging.basicConfig(format='%(levelname)s:%(pathname)s:%(lineno)d | %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug('start')



import sqlalchemy
import mysql.connector
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base() # magic
import sqlalchemy.orm


sqlite = 'sqlite:///:memory:'
mysql = 'mysql+mysqlconnector://mcarifio:123456@localhost/sqla'

engines = []
for c in [sqlite, mysql]:
    engine = sqlalchemy.create_engine(c, echo=True)
    logger.debug(engine)
    engines.append(engine)

import sqlalchemy.types as types
import uuid

class UUID(types.TypeDecorator):
    impl = types.LargeBinary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and isinstance(value, string):
            return uuid.UUID(value).bytes
        elif value:
            raise ValueError('value %s is not a valid uuid.UUId' % value)
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False


from sqlalchemy import Column, Integer, String
# Needs a UUID type for primary key
class Merchant(Base):
    __tablename__ = 'Merchant' # TODO from classname?

    # @staticmethod
    # def __new__(cls, *args, **kwargs):
    #     cls.__tablename__ = cls.__name__

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))

    def __repr__(self):
        return '<{cls}(id={id}, name={name}>'.format(cls=self.__class__.__name__, id=self.id, name=self.name)


# Write a DDL utility? Does each class load itself? How about altering class changes?

for engine in engines:
    Base.metadata.create_all(engine) # is this persistent?

merchants = [Merchant(name=m) for m in ['m%d' % (i) for i in range(5)]]

sessions = [(sqlalchemy.orm.sessionmaker(bind=engine))() for engine in engines]
# for s in sessions:
#     s.add_all(merchants)
#     s.commit()


sessions[1].add_all(merchants)
sessions[1].commit()

for m in merchants: print(m)

