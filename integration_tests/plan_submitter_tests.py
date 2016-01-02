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
                    "id": "2",
                    "start_on": "2066-12-11T23:14:15.554Z",
                    "name": "namename"
                },
                {
                    "id": "3",
                    "start_on": "2066-12-11T23:14:15.554Z",
                    "name": "namename"
                },
                {
                    "id": "4",
                    "start_on": "2066-12-11T23:14:15.554Z",
                    "name": "namename"
                },
                {
                    "id": "5",
                    "start_on": "2066-12-11T23:14:15.554Z",
                    "name": "namename"
                }
            ],
            "dependencies": [
                {
                    "from": "1",
                    "to": "2"
                },
                {
                    "from": "1",
                    "to": "3"
                },
                {
                    "from": "2",
                    "to": "5"
                },
                {
                    "from": "3",
                    "to": "4"
                },
                {
                    "from": "4",
                    "to": "5"
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
        self.assertEqual(len(plan.get_tasks()), 5)

    def test_plan_is_running(self):
        plan = parse_plan_json(plan_json1)
        result = store_new_plan.delay(plan)

        plan_id = result.get(5)

        for i in xrange(55):
            time.sleep(1)
            if self.plan_repo.get_plan_by_id(plan_id).is_plan_running():
                return

        self.assertTrue(self.plan_repo.get_plan_by_id(plan_id).is_plan_running())

    def test_run_tasks(self):
        plan = parse_plan_json(plan_json1)
        result = store_new_plan.delay(plan)

        plan_id = result.get(5)
        
        def assert_task_ids_in_list(actual_tasks_list, assertion_task_id_list):
            self.assertListEqual(
                map(lambda t: t.get_task_id(), actual_tasks_list),
                assertion_task_id_list
            )

        def get_running_tasks():
            time.sleep(12)
            tasks = self.task_repo.get_tasks(plan_id)
            return filter(lambda t: t.is_task_running(), tasks)

        task_list = self.task_repo.get_tasks(plan_id)

        task1 = task_list[0]
        task2 = task_list[1]
        task3 = task_list[2]
        task4 = task_list[3]
        task5 = task_list[4]

        task_list_1 = get_running_tasks()
        assert_task_ids_in_list(task_list_1, ["1"])

        task1.set_task_as_complete()
        self.task_repo.save_task(plan_id, task1)

        task_list_2 = get_running_tasks()
        assert_task_ids_in_list(task_list_2, ["2", "3"])

        task2.set_task_as_complete()
        self.task_repo.save_task(plan_id, task2)

        task_list_3 = get_running_tasks()
        assert_task_ids_in_list(task_list_3, ["3"])

        task3.set_task_as_complete()
        self.task_repo.save_task(plan_id, task3)

        task_list_4 = get_running_tasks()
        assert_task_ids_in_list(task_list_4, ["4"])

        task4.set_task_as_complete()
        self.task_repo.save_task(plan_id, task4)

        task_list_5 = get_running_tasks()
        assert_task_ids_in_list(task_list_5, ["5"])

        task5.set_task_as_complete()
        self.task_repo.save_task(plan_id, task5)

        task_list_6 = get_running_tasks()
        assert_task_ids_in_list(task_list_6, [])
