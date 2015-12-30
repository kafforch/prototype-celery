#!/usr/bin/env bash

# Env vars
REDIS_PATH=/Users/michaelhyatt/work/kafforch/redis-3.0.6
REDIS_SERVER_CMD=src/redis-server
REDIS_CLI_CMD=src/redis-cli
VIRTUALENV_PATH=/Users/michaelhyatt/kafforch-celery
PROJECT_DIR=/Users/michaelhyatt/work/kafforch/prototype-celery
UTRUNNER="/Applications/PyCharm CE.app/Contents/helpers/pycharm/utrunner.py"

# Start Redis
cd $REDIS_PATH
nohup $REDIS_SERVER_CMD &
sleep 5

# Start celery worker
cd $PROJECT_DIR
source $VIRTUALENV_PATH/bin/activate
nohup celery worker -A workers.base -l info -B &
sleep 5

# Run tests
cd $PROJECT_DIR
source $VIRTUALENV_PATH/bin/activate
export PYTHONPATH=$PYTHONPATH:$PROJECT_DIR
$VIRTUALENV_PATH/bin/python "$UTRUNNER" $PROJECT_DIR/cfg/_args_separator_live_test.py true
sleep 2

# Stop celery worker
res=$(ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -9)
sleep 2

# Stop redis
cd $REDIS_PATH
$REDIS_CLI_CMD shutdown &
sleep 5


