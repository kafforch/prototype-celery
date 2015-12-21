from cfg.celery_config import app
from model import plan_repo, task_repo


@app.task
def store_plan(plan):
    plan_repo.save(plan)
    task_repo.save()


