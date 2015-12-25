import unittest
from model import plan_repo_factory, task_repo
import mock
from workers import plan_submitter

plan_repo = plan_repo_factory.factory("TEST")

class DummyPlan:
    def __init__(self, plan_id, tasks, dependencies):
        self.plan_id = plan_id
        self.tasks = tasks
        self.dependencies = dependencies

    def get_plan_id(self):
        return self.plan_id

    def get_dependencies(self):
        return self.dependencies

    def get_tasks(self):
        return self.tasks

    def set_plan_id(self, plan_id):
        self.plan_id = plan_id


class PlanRepoTests(unittest.TestCase):
    def setUp(self):
        plan_repo.purge_all_plans()
        plan1 = DummyPlan(1,[1,2,3],[4,5])
        plan2 = DummyPlan(2, [4,5], [6])
        plan_repo.save(plan1)
        plan_repo.save(plan2)

    def test_get_by_id_success(self):
        self.assertIsInstance(plan_repo.get_plan_by_id(1), DummyPlan)
        self.assertIsInstance(plan_repo.get_plan_by_id(2), DummyPlan)

    def test_get_by_id_failure(self):
        self.assertIsNone(plan_repo.get_plan_by_id(3))

    def test_get_number_of_plans(self):
        self.assertEqual(plan_repo.get_number_of_plans(), 2)


class CeleryPlanRepoTests(unittest.TestCase):

    def setUp(self):
        plan_repo.purge_all_plans()
        task_repo.purge_all_dependencies()
        task_repo.purge_all_tasks()

    def test_celery_save_plan(self):

        plan1 = DummyPlan(1, [5,6], [7])
        plan_id = plan_repo.get_id()
        plan1.set_plan_id(plan_id)

        self.assertEqual(plan_repo.get_number_of_plans(), 0)

        with mock.patch('cfg.celery_config.CELERY_ALWAYS_EAGER', True, create=True):
            plan_submitter.store_plan(plan1)

        self.assertIsInstance(plan_repo.get_plan_by_id(plan_id), DummyPlan)
        self.assertIsNone(plan_repo.get_plan_by_id(999), DummyPlan)
        self.assertEqual(plan_repo.get_number_of_plans(), 1)
        self.assertEqual(task_repo.get_number_of_tasks(), 2)
        self.assertEqual(task_repo.get_number_of_dependencies(), 1)

