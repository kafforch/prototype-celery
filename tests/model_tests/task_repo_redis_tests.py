import unittest
from model import task_repo_redis, plan_parser
import fakeredis

task_repo = task_repo_redis.TaskRepo(fakeredis.FakeStrictRedis())

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


class TaskRepoTests(unittest.TestCase):
    def setUp(self):
        task_repo.purge_all_tasks()
        task_repo.purge_all_dependencies()
        plan = plan_parser.parse_plan_json(plan_json1)
        task_repo.save_dependencies('123', plan.get_dependencies())
        task_repo.save_tasks('123', plan.get_tasks())

    def tearDown(self):
        task_repo.purge_all_tasks()
        task_repo.purge_all_dependencies()

    def test_get_tasks_back_success(self):
        tasks = task_repo.get_tasks('123')
        self.assertListEqual(["task1", "namename", "namename123"], \
                             map(lambda t: t.get_name(), tasks))

    def test_get_dependencies_back_success(self):
        deps = task_repo.get_dependencies('123')
        self.assertListEqual(["2", "3"], \
                             map(lambda t: t.get_to(), deps))

    def test_get_number_of_tasks(self):
        self.assertEqual(task_repo.get_number_of_tasks('123'), 3)

    def test_get_number_of_dependencies(self):
        self.assertEqual(task_repo.get_number_of_dependencies('123'), 2)
