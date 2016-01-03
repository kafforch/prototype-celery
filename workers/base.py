from celery.signals import celeryd_after_setup
from redis import StrictRedis
from redlock import RedLockFactory

from utils.config import KafforchConfigurator
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo

from celery import Celery
from utils.config import KafforchConfigurator
from utils.file_utils import find

class Repo:
    pass


repo = Repo()
repo.plan_repo = None
repo.task_repo = None

repo.config = KafforchConfigurator(find("kafforch.cfg", ".."))
redis_config = repo.config.get_redis_config_kwargs()
celery_config = repo.config.get_celery_config_dict()

app = Celery()
app.conf.update(**celery_config)

def lock(lock_name):
    return RedLockFactory(
            connection_details=[redis_config]) \
        .create_lock(lock_name,
                     ttl=int(repo.config.get_value("Redlock", "ttl")),
                     retry_times=int(repo.config.get_value("Redlock",
                                                           "retry_times")),
                     retry_delay=int(repo.config.get_value("Redlock",
                                                           "retry_delay"))
                     )


redis_inst = StrictRedis(**redis_config)


@celeryd_after_setup.connect()
def init(sender, instance, **kwargs):
    repo.plan_repo = PlanRepo(redis_inst)
    repo.task_repo = TaskRepo(redis_inst)
