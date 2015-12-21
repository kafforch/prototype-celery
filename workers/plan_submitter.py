from cfg.celery_config import app
from model import plan_repo, task_repo
import uuid

@app.task
def store_plan(plan):
    plan_id = uuid.uuid4()
    plan.set_plan_id(plan_id)
    plan_repo.save(plan)
    task_repo.save_tasks(plan_id, plan.get_tasks())
    task_repo.save_dependencies(plan_id, plan.get_dependencies())
    return plan_id

