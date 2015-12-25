from workers import plan_submitter
from model import plan_parser, plan_repo
from cfg import celery_config
import fakeredis
import unittest
import uuid
import mock

plan_repo = plan_repo.PlanRepo(fakeredis.FakeStrictRedis())

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


class PlanRepoLocalTests(unittest.TestCase):
    def setUp(self):
        plan_repo.purge_all_plans()

    def test_plan_repo_locally_first(self):
        built_plan = plan_parser.parse_plan_json(plan_json1)

        plan_id = plan_repo.get_id()

        self.assertIsNotNone(plan_id)

        built_plan.set_plan_id(plan_id)

        plan_repo.save(built_plan)

        plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()), 2)

class PlanSubmitterTests(unittest.TestCase):

    @unittest.skip("")
    def test_plan_submission1(self):

        built_plan = plan_parser.parse_plan_json(plan_json1)

        with mock.patch('cfg.celery_config.CELERY_ALWAYS_EAGER', True, create=True):
            plan_id = plan_submitter.store_plan(built_plan)

        plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()), 2)
