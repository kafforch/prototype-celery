from unittest import TestCase, TestLoader
from cfg.config import KafforchConfigurator
import os

# Ensuring ordered execution of tests
TestLoader.sortTestMethodsUsing = None

func_test_config = KafforchConfigurator("cfg/kafforch.cfg")

class BaseFunctionalTestCase(TestCase):
    @classmethod
    def setUpClass(cls):

        start_cmd = '''
            # Start Redis
            res=$(ps auxww | grep 'redis-server' | grep -v grep | awk '{{print $2}}' | xargs kill -9)
            nohup {0}/src/redis-server &
            sleep 5

            # Start celery worker
            cd {2}
            source {1}/bin/activate
            nohup celery worker -A workers.base -l info -B &
            sleep 5

        '''.format(
            func_test_config.get_value("Functional-Tests", "redispath"),
            func_test_config.get_value("Functional-Tests", "virtualenvpath"),
            func_test_config.get_value("Functional-Tests", "projectdir")
        )
        os.system(start_cmd)

    @classmethod
    def tearDownClass(cls):

        stop_cmd = '''
            # Stop celery worker
            res=$(ps auxww | grep 'celery worker' | grep -v grep | awk '{{print $2}}' | xargs kill -9)
            sleep 2

            # Stop redis
            {0}/src/redis-cli shutdown &
            sleep 5
        '''.format(
            func_test_config.get_value("Functional-Tests", "redispath")
        )
        os.system(stop_cmd)
