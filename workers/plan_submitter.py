from celery import Celery
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
from redis import StrictRedis
from workers.config import WorkerConfigurator
from celery.signals import celeryd_after_setup

config = WorkerConfigurator("cfg/kafforch.cfg")

celery_config = config.get_celery_config_kwargs()
redis_config = config.get_redis_config_kwargs()

redis_inst = StrictRedis(**redis_config)

app = Celery(**celery_config)


class Repo:
    pass


repo = Repo()
repo.plan_repo = None
repo.task_repo = None


@celeryd_after_setup.connect()
def init(sender, instance, **kwargs):
    repo.plan_repo = PlanRepo(redis_inst)
    repo.task_repo = TaskRepo(redis_inst)


@app.task()
def store_plan(plan):
    plan_id = repo.plan_repo.save_new_plan(plan)
    repo.task_repo.save_new_tasks(plan_id, plan.get_tasks())
    repo.task_repo.save_dependencies(plan_id, plan.get_dependencies())
    return plan_id
