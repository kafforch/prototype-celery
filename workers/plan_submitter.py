from celery_cfg.celery_config import app
from model import plan_repo, task_repo


@app.task
def store_plan(plan):
    plan_repo.save(plan)


@app.task
def retrieve_plan(plan_id):
    return plan_repo.get_by_id(plan_id)
