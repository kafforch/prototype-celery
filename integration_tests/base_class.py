from unittest import TestCase, TestLoader
import os
from utils.config import KafforchConfigurator

# Ensuring ordered execution of tests
TestLoader.sortTestMethodsUsing = None

func_test_config = KafforchConfigurator("integration_tests/kafforch_test.cfg")


class BaseIntegrationTestCase(TestCase):

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
            nohup celery worker -A workers.base -l info -B -n worker1.%h &
            nohup celery worker -A workers.base -l info -B -n worker2.%h &
            nohup celery worker -A workers.base -l info -B -n worker3.%h &
            nohup celery worker -A workers.base -l info -B -n worker4.%h &
            nohup celery worker -A workers.base -l info -B -n worker5.%h &
            nohup celery worker -A workers.base -l info -B -n worker6.%h &
            nohup celery worker -A workers.base -l info -B -n worker7.%h &
            nohup celery worker -A workers.base -l info -B -n worker8.%h &
            nohup celery worker -A workers.base -l info -B -n worker9.%h &
            nohup celery worker -A workers.base -l info -B -n worker10.%h &
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