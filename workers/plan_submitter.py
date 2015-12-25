from cfg.celery_config import app
from model.plan_repo import PlanRepo
from model.task_repo import TaskRepo
import logging

class Repos:
    pass

repos = Repos()

def set_repos(in_redis):
    repos.plan_repo = PlanRepo(in_redis)
    repos.task_repo = TaskRepo(in_redis)

@app.task()
def store_plan(plan):
    plan_id = repos.plan_repo.save(plan)
    logger = logging.getLogger(__name__)
    logger.debug("Saving plan with id:{}".format(plan_id))
    repos.task_repo.save_tasks(plan_id, plan.get_tasks())
    repos.task_repo.save_dependencies(plan_id, plan.get_dependencies())
    return plan_id
