from model import plan_parser, plan_repo, task_repo
import fakeredis
import unittest

plan_repo = plan_repo.PlanRepo(fakeredis.FakeStrictRedis())
task_repo = task_repo.TaskRepo(fakeredis.FakeStrictRedis())

plan_json1 = '''{
            "start_on": "2015-12-11T23:14:15.554Z",
            "tasks": [
                {
                    "task_id": "1",
                    "name": "task1",
                    "test": "test123"
                },
                {
                    "task_id": "2",
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

        plan_repo.save_new_plan(built_plan)
        task_repo.save_new_tasks(plan_id, built_plan.get_tasks())
        task_repo.save_dependencies(plan_id, built_plan.get_dependencies())

        plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()), 2)

    def test_plan_submission1(self):
        built_plan = plan_parser.parse_plan_json(plan_json1)

        plan_id = plan_repo.save_new_plan(built_plan)
        task_repo.save_new_tasks(plan_id, built_plan.get_tasks())
        task_repo.save_dependencies(plan_id, built_plan.get_dependencies())

        plan = plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()), 2)
