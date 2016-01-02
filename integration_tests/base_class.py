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
            res=$(ps auxww | grep 'celery worker' | grep -v grep | awk '{{print $2}}' | xargs kill -9)
            nohup {0}/src/redis-server &
            sleep 3

            # Start celery worker
            cd {2}
            source {1}/bin/activate
            nohup celery worker -A workers.application -l info -n app1.%h -Q app &
            nohup celery worker -A workers.application -l info -n app2.%h -Q app &
            nohup celery worker -A workers.application -l info -n app3.%h -Q app &
            sleep 1
            nohup celery worker -A workers.plan_periodic -l info -B -n plan1.%h -Q plans &
            sleep 1
            nohup celery worker -A workers.task_periodic -l info -B -n task1.%h -Q tasks &
            sleep 3

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