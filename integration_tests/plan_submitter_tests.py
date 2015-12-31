from integration_tests.base_class import BaseIntegrationTestCase
from workers.plan_submitter import store_new_plan
from model.plan_parser import parse_plan_json
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
from redis import Redis
import time


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
                },
                {
                    "id": "27",
                    "start_on": "2026-12-11T23:14:15.554Z",
                    "name": "namename123"
                }
            ],
            "dependencies": [
                {
                    "from": "1",
                    "to": "2"
                },
                {
                    "from": "2",
                    "to": "3"
                }
            ]
            }'''


class PlanSubmitterTests(BaseIntegrationTestCase):
    def setUp(self):
        self.plan_repo = PlanRepo(Redis("localhost"))
        self.plan_repo.purge_all_plans()
        self.plan_repo.reset_id()

        self.task_repo = TaskRepo(Redis("localhost"))
        self.task_repo.purge_all_tasks()
        self.task_repo.purge_all_dependencies()

    def test_submit_plan(self):
        plan = parse_plan_json(plan_json1)
        result = store_new_plan.delay(plan)

        plan_id = result.get(5)

        self.assertEqual(plan_id, 'c4ca4238a0b923820dcc509a6f75849b')

        plan = self.plan_repo.get_plan_by_id(plan_id)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.get_tasks()), 3)

    def test_plan_is_running(self):
        plan = parse_plan_json(plan_json1)
        result = store_new_plan.delay(plan)

        plan_id = result.get(5)

        for i in xrange(11):
            time.sleep(1)
            if self.plan_repo.get_plan_by_id(plan_id).is_plan_running():
                return

        self.assertTrue(self.plan_repo.get_plan_by_id(plan_id).is_plan_running())


