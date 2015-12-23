from workers import plan_submitter
from model import plan_parser, plan_repo, task_repo
from celerytest.testcase import CeleryTestCaseMixin, start_celery_worker
from unittest import TestCase
import uuid
import time

from cfg.celery_config import app

REDIS_INSTALL_DIR = '/Users/michaelhyatt/work/kafforch/redis-3.0.6/'

start_celery_worker(app)

plan_json1 = '''{
            "start_on": "2015-12-11T23:14:15.554Z",
            "tasks": [
                {
                    "id": "1",
                    "name": "task1",
                    "test": "test123"
                },
                {
                    "id": "23",
                    "start_on": "2066-12-11T23:14:15.554Z",
                    "name": "namename"
                }
            ],
            "dependencies": [
                {
                    "from": "1",
                    "to": "2"
                }
            ]
            }'''


class PlanSubmitterTests(CeleryTestCaseMixin, TestCase):
    celery_app = app
    celery_concurrency = 4

    def test_plan_submission1(self):
        built_plan = plan_parser.parse_plan_json(plan_json1)

        plan_id_async = plan_submitter.store_plan.apply(built_plan)

        plan_id = str(plan_id_async)

        self.assertEqual(len(str(uuid.uuid4())), len(plan_id))

        self.worker.idle.wait()

        plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()),2)
