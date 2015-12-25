import unittest
import mock
import logging

from model import plan_parser, plan_repo_simple, task_repo
from workers import plan_submitter

json_string = '''{
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


class PlanParserTests(unittest.TestCase):
    def setUp(self):
        plan_repo_simple.purge_all_plans()

    def test_parsing1(self):
        plan = plan_parser.parse_plan_json(json_string)
        self.assertTrue(plan.get_dependencies()[0].get_from() == "1")
        self.assertTrue(plan.get_dependencies()[0].get_to() == "2")
        self.assertTrue(plan.get_tasks()[0].get_task_id() == "1")
        self.assertTrue(plan.get_tasks()[1].get_task_id() == "23")
        self.assertTrue(plan.get_start_on() == "2015-12-11T23:14:15.554Z")

    def test_repo_with_parser1(self):
        plan = plan_parser.parse_plan_json(json_string)

        with mock.patch('cfg.celery_config.CELERY_ALWAYS_EAGER', True, create=True):
            plan_id = plan_submitter.store_plan(plan)

        saved_plan = plan_repo_simple.get_plan_by_id(plan_id)

        self.assertIsNotNone(saved_plan)
        self.assertTrue(saved_plan.get_plan_id() == plan_id)
        self.assertTrue(saved_plan.get_start_on() == "2015-12-11T23:14:15.554Z")
        self.assertTrue(len(saved_plan.get_tasks()) == 2)
        self.assertTrue(len(saved_plan.get_dependencies()) == 1)

        self.assertIsNotNone(task_repo.get_dependency(plan_id, "1", "2"))
        self.assertIsNone(task_repo.get_dependency(plan_id, "5", "6"))
        self.assertIsNotNone(task_repo.get_task_by_id(plan_id, "23"))
        self.assertTrue(task_repo.get_task_by_id(plan_id, "23").get_start_on() == \
                        "2066-12-11T23:14:15.554Z")
        self.assertIsNone(task_repo.get_task_by_id(plan_id, "215"))

    def test_repo_with_parser2(self):
        plan = plan_parser.parse_plan_json(json_string)
        plan_id = plan_repo_simple.get_id()
        plan.set_plan_id(plan_id)

        with mock.patch('cfg.celery_config.CELERY_ALWAYS_EAGER', True, create=True):
            plan_id = plan_submitter.store_plan(plan)

        saved_plan = plan_repo_simple.get_plan_by_id(plan_id)

        self.assertIsNotNone(saved_plan)
        self.assertTrue(saved_plan.get_plan_id() == plan_id)
        self.assertTrue(saved_plan.get_start_on() == "2015-12-11T23:14:15.554Z")
        self.assertTrue(len(saved_plan.get_tasks()) == 2)
        self.assertTrue(len(saved_plan.get_dependencies()) == 1)

        self.assertIsNotNone(task_repo.get_dependency(plan_id, "1", "2"))
        self.assertIsNone(task_repo.get_dependency(plan_id, "5", "6"))
        self.assertIsNotNone(task_repo.get_task_by_id(plan_id, "23"))
        self.assertTrue(task_repo.get_task_by_id(plan_id, "23").get_start_on() == \
                        "2066-12-11T23:14:15.554Z")
        self.assertIsNone(task_repo.get_task_by_id(plan_id, "215"))
