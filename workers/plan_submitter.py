from celery.contrib.methods import task_method
from cfg.celery_config import app
from celery import current_app
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
from redis import Redis


class PlanSubmitter(object):

    def __init__(self, redisconf):
        self.__redisconf = redisconf

    @current_app.task(filter=task_method)
    def store_plan(self, plan):
        plan_repo = PlanRepo(in_redis=Redis(self.__redisconf))
        task_repo = TaskRepo(in_redis=Redis(self.__redisconf))
        plan_id = plan_repo.save(plan)
        task_repo.save_tasks(plan_id, plan.get_tasks())
        task_repo.save_dependencies(plan_id, plan.get_dependencies())
        return plan_id
