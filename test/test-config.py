import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler()) # log to stderr

import unittest

import config

class ConfigTestCase(unittest.TestCase):

    success_case = """
# Well-formed yaml file

production:
    title: "Used in production"
    database:
        read_write: mysql://production_boy:production_password@db.host.com/rwdb # read-write
        read_only: mysql://read_only_boy:readable_pass@db.host.com/rodb # read-only

development:
    title: "Used in development"
    database:
        read_write: mysql://dev_boy:dev_pass@localhost/dbhost # read-write
        read_only: mysql://dev_boy:devpass@localhost/pazien # read-only
            """


    def test_true(self):
        """Test the test runner"""
        self.assertTrue(True)


    def test_success_path(self):
        """Parse an expected yaml configuration string."""
        c = config.Configurations(config.attrdict_from_yaml_string(self.success_case))
        self.assertTrue(c.select('production'))
        self.assertTrue(c.select('development'))
        self.assertTrue(c.production)
        self.assertTrue(c.production.database)

    def test_slices(self):
        c = config.Configurations(config.attrdict_from_yaml_string(self.success_case))
        for kind in c:
            self.assertTrue(kind.database.read_write)
            self.assertTrue(kind.database.read_only)


    def test_parts_attribute_selection(self):
        c = config.Configurations(config.attrdict_from_yaml_string(self.success_case)).production
        self.assertTrue(c.database)
        self.assertTrue(c.database.read_write)
        try:
            c.development
        except AttributeError as ae:
            self.assertTrue(True, "Expecting AttributeError")
        except Exception as e:
            self.fail("Not expecting generic Exception")

    def test_parts(self):
        c = config.Configurations(config.attrdict_from_yaml_string(self.success_case)).select('production')
        self.assertTrue(c.database)
        self.assertTrue(c.database.read_write)
        try:
            c.development
        except AttributeError as ae:
            self.assertTrue(True, "Expecting AttributeError")
        except Exception as e:
            self.fail("Not expecting generic Exception")


# print(c.production.database.read_write)
#
# # the "top" level attributes in the Configuration are considered its "keys", i.e. 'production' and 'development'
# # TODO: pycharm completes these names?
# for k in c:
#     print(k, c[k].database, c[k].database.read_write)
#
# # and finally
# env = os.environ.get("APP_ENV", "development")
# print(c[env].database.read_write)




if __name__ == '__main__':
    unittest.main()
