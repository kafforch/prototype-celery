from unittest import TestCase
import os


class BaseFunctionalTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        start_cmd = '''
            #!/usr/bin/env bash

            # Env vars
            REDIS_PATH=/Users/michaelhyatt/work/kafforch/redis-3.0.6
            REDIS_SERVER_CMD=src/redis-server
            VIRTUALENV_PATH=/Users/michaelhyatt/kafforch-celery
            PROJECT_DIR=/Users/michaelhyatt/work/kafforch/prototype-celery

            # Start Redis
            cd $REDIS_PATH
            nohup $REDIS_SERVER_CMD &
            sleep 5

            # Start celery worker
            cd $PROJECT_DIR
            source $VIRTUALENV_PATH/bin/activate
            nohup celery worker -A workers.base -l info -B &
            sleep 5

        '''
        os.system(start_cmd)

    @classmethod
    def tearDownClass(cls):
        stop_cmd = '''
            # Env
            REDIS_PATH=/Users/michaelhyatt/work/kafforch/redis-3.0.6
            REDIS_CLI_CMD=src/redis-cli

            # Stop celery worker
            res=$(ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -9)
            sleep 2

            # Stop redis
            cd $REDIS_PATH
            $REDIS_CLI_CMD shutdown &
            sleep 5
        '''
        os.system(stop_cmd)
