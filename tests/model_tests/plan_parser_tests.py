import unittest
import fakeredis
from model import plan_parser, plan_repo, task_repo

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

plan_repo = plan_repo.PlanRepo(fakeredis.FakeStrictRedis())
task_repo = task_repo.TaskRepo(fakeredis.FakeStrictRedis())

class PlanParserTests(unittest.TestCase):
    def setUp(self):
        plan_repo.purge_all_plans()

    def test_parsing1(self):
        plan = plan_parser.parse_plan_json(json_string)
        self.assertTrue(plan.get_dependencies()[0].get_from() == "1")
        self.assertTrue(plan.get_dependencies()[0].get_to() == "2")
        self.assertTrue(plan.get_tasks()[0].get_task_id() == "1")
        self.assertTrue(plan.get_tasks()[1].get_task_id() == "23")
        self.assertTrue(plan.get_start_on() == "2015-12-11T23:14:15.554Z")

    def test_repo_with_parser1(self):
        plan = plan_parser.parse_plan_json(json_string)

        plan_id = plan_repo.save_new_plan(plan)
        task_repo.save_new_tasks(plan_id, plan.get_tasks())
        task_repo.save_dependencies(plan_id, plan.get_dependencies())

        saved_plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(saved_plan)
        self.assertTrue(saved_plan.get_plan_id() == plan_id)
        self.assertTrue(saved_plan.get_start_on() == "2015-12-11T23:14:15.554Z")
        self.assertTrue(len(saved_plan.get_tasks()) == 2)
        self.assertTrue(len(saved_plan.get_dependencies()) == 1)

        self.assertEqual(len(task_repo.get_dependencies(plan_id)), 1)
        self.assertEqual(len(task_repo.get_tasks(plan_id)), 2)
        self.assertTrue(task_repo.get_tasks(plan_id)[1].get_start_on() == \
                        "2066-12-11T23:14:15.554Z")
        self.assertTrue(task_repo.get_tasks(plan_id)[1].is_task_initial())

    def test_repo_with_parser2(self):
        plan = plan_parser.parse_plan_json(json_string)
        plan_id = plan_repo.get_id()
        plan.set_plan_id(plan_id)

        plan_id = plan_repo.save_new_plan(plan)
        task_repo.save_new_tasks(plan_id, plan.get_tasks())
        task_repo.save_dependencies(plan_id, plan.get_dependencies())

        saved_plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(saved_plan)
        self.assertTrue(saved_plan.get_plan_id() == plan_id)
        self.assertTrue(saved_plan.get_start_on() == "2015-12-11T23:14:15.554Z")
        self.assertTrue(len(saved_plan.get_tasks()) == 2)
        self.assertTrue(len(saved_plan.get_dependencies()) == 1)

        self.assertEqual(len(task_repo.get_dependencies(plan_id)), 1)
        self.assertEqual(len(task_repo.get_tasks(plan_id)), 2)
        self.assertTrue(task_repo.get_tasks(plan_id)[1].get_start_on() == \
                        "2066-12-11T23:14:15.554Z")
