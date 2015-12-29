import unittest
from workers.base import BaseWorker
import os

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.base = BaseWorker("../../cfg/kafforch.cfg")

    def test_loading_properties(self):
        self.assertIsNotNone(self.base)

    def test_celery_config(self):
        celery_config = self.base.get_celery_config_kwargs()

        self.assertIsNotNone(celery_config)
        self.assertEqual(len(celery_config.keys()),2)