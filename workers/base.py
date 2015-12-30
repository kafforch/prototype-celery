from celery import Celery
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
from redis import StrictRedis
from workers.config import WorkerConfigurator
from celery.signals import celeryd_after_setup
from redlock import RedLock


class Repo:
    pass


repo = Repo()
repo.plan_repo = None
repo.task_repo = None


repo.config = WorkerConfigurator("cfg/kafforch.cfg")

redis_config = repo.config.get_redis_config_kwargs()
redis_inst = StrictRedis(**redis_config)

celery_config = repo.config.get_celery_config_dict()
app = Celery()
app.conf.update(**celery_config)


@celeryd_after_setup.connect()
def init(sender, instance, **kwargs):
    repo.plan_repo = PlanRepo(redis_inst)
    repo.task_repo = TaskRepo(redis_inst)
    repo.dlm = RedLock([redis_config])


