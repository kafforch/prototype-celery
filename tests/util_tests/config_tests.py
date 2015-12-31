import unittest

from utils.config import KafforchConfigurator


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.base = KafforchConfigurator("cfg/kafforch.cfg")

    def test_loading_properties(self):
        self.assertIsNotNone(self.base)

    def test_celery_config(self):
        celery_config = self.base.get_celery_config_dict()

        self.assertIsNotNone(celery_config)
        self.assertGreater(len(celery_config.keys()), 2)
