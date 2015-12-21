import unittest
from model import plan_repo
import mock
from celery_cfg import celery_config


class DummyPlan:
    def __init__(self, plan_id):
        self.plan_id = plan_id

    def get_id(self):
        return self.plan_id


class PlanRepoTests(unittest.TestCase):
    def setUp(self):
        plan_repo.purge_all_plans()
        plan1 = DummyPlan(1)
        plan2 = DummyPlan(2)
        plan_repo.save(plan1)
        plan_repo.save(plan2)

    def test_get_by_id_success(self):
        self.assertIsInstance(plan_repo.get_by_id(1), DummyPlan)
        self.assertIsInstance(plan_repo.get_by_id(2), DummyPlan)

    def test_get_by_id_failure(self):
        self.assertIsNone(plan_repo.get_by_id(3))

    def test_get_number_of_plans(self):
        self.assertEqual(plan_repo.get_number_of_plans(), 2)


class CeleryPlanRepoTests(unittest.TestCase):
    def test_celery_save_plan(self):

        plan1 = DummyPlan(1)

        with mock.patch('celery_cfg.celery_config.CELERY_ALWAYS_EAGER', True, create=True):
            plan_repo.save(plan1)

