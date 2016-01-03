import unittest
from model import plan_repo, plan_parser, task_repo
import fakeredis

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

plan_repo = plan_repo.PlanRepo(fakeredis.FakeStrictRedis())
task_repo = task_repo.TaskRepo(fakeredis.FakeStrictRedis())


class PlanRepoRedisTests(unittest.TestCase):
    def setUp(self):
        plan_repo.purge_all_plans()
        self.plan1 = plan_parser.parse_plan_json(plan_json1)
        self.plan2 = plan_parser.parse_plan_json(plan_json1)

    def test_get_by_id_success(self):

        self.assertEqual(plan_repo.get_number_of_plans(), 0)

        plan_id = plan_repo.save_new_plan(self.plan1)
        self.assertIsNotNone(plan_id)
        task_repo.save_new_tasks(plan_id, self.plan1.get_tasks())
        task_repo.save_dependencies(plan_id, self.plan1.get_dependencies())

        plan2 = plan_repo.get_plan_by_id(plan_id)
        self.assertIsNotNone(plan2)
        self.assertTrue(plan2.is_plan_initial())
        self.assertEqual(plan_id, plan2.get_plan_id())
        self.assertEqual(len(plan2.get_dependencies()), 1)
        self.assertEqual(len(plan2.get_tasks()), 2)

        self.assertEqual(plan_repo.get_number_of_plans(), 1)

        plan_repo.purge_all_plans()

        self.assertEqual(plan_repo.get_number_of_plans(), 0)

    def test_for_more_than_one_plan(self):
        plan_repo.save_new_plan(self.plan1)
        plan_repo.save_new_plan(self.plan2)
        self.assertEqual(plan_repo.get_number_of_plans(), 2)
        plan_repo.purge_all_plans()
        self.assertEqual(plan_repo.get_number_of_plans(), 0)
