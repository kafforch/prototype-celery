from workers.base import app, repo
from celery.utils.log import get_task_logger
from celery.schedules import timedelta

TASK_NAME = '{}.start_plans'.format(__name__)

logger = get_task_logger(__name__)

app.conf.CELERYBEAT_SCHEDULE.update(
    dict(
        start_plans=dict(
            task=TASK_NAME,
            schedule=timedelta(seconds=repo.config.get_plan_starter_cycle_time())
        )
    )
)

@app.task()
def start_plans():
    logger.info("Running start_plans")
    for plan_id in repo.plan_repo.get_all_plan_ids():
        plan = repo.plan_repo.get_plan_by_id(plan_id)
        if plan.is_plan_initial():
            with repo.dlm:
                logger.info("Starting plan {}".format(plan_id))
                plan.set_plan_as_running()
                repo.plan_repo.save_plan(plan_id, plan)
