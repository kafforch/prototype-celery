from cfg.celery_config import app
from model import plan_repo_simple, task_repo_simple
import logging


@app.task()
def store_plan(plan):
    plan_id = plan_repo_simple.save(plan)
    logger = logging.getLogger(__name__)
    logger.debug("Saving plan with id:{}".format(plan_id))
    task_repo_simple.save_tasks(plan_id, plan.get_tasks())
    task_repo_simple.save_dependencies(plan_id, plan.get_dependencies())
    return plan_id
