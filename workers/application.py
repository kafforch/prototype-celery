from workers.base import repo, app
from celery.utils.log import get_task_logger
from utils.time_utils import utcnow_str

logger = get_task_logger(__name__)


@app.task()
def store_new_plan(plan):
    plan.set_submitted_on(utcnow_str())
    plan_id = repo.plan_repo.save_new_plan(plan)
    repo.task_repo.save_new_tasks(plan_id, plan.get_tasks())
    repo.task_repo.save_dependencies(plan_id, plan.get_dependencies())
    return plan_id


@app.task()
def complete_task(plan_id, task_id):
    logger.info("Completing task {0} for plan {1}".format(task_id, plan_id))
    task = repo.task_repo.get_task(plan_id, task_id)
    task.set_completed_on(utcnow_str())
    task.set_task_as_complete()
    result = repo.task_repo.save_task(plan_id, task)
    return result
