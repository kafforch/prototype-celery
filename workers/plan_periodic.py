from workers.base import repo, app
from celery.utils.log import get_task_logger
from celery.schedules import timedelta
from utils.time_utils import is_time_in_the_past
from model.task_starter_logic import all_tasks_complete
from utils.time_utils import utcnow_str

START_PLANS_TASK_NAME = '{}.start_plans'.format(__name__)
COMPLETE_PLANS_TASK_NAME = '{}.complete_plans'.format(__name__)

logger = get_task_logger(__name__)

app.conf.CELERYBEAT_SCHEDULE.update(
        dict(
                start_plans=dict(
                        task=START_PLANS_TASK_NAME,
                        schedule=timedelta(seconds=repo.config.get_plan_handler_cycle_time())
                ),
                complete_plans=dict(
                        task=COMPLETE_PLANS_TASK_NAME,
                        schedule=timedelta(seconds=repo.config.get_plan_handler_cycle_time())
                )

        )
)


@app.task()
def start_plans():
    logger.info("Running start_plans")
    for plan_id in repo.plan_repo.get_all_plan_ids():
        plan = repo.plan_repo.get_plan_by_id(plan_id)
        if plan.is_plan_initial():
            if plan.get_start_on() is None \
                    or is_time_in_the_past(plan.get_start_on()):
                    logger.info("Starting plan {}".format(plan_id))
                    plan.set_started_on(utcnow_str())
                    plan.set_plan_as_running()
                    repo.plan_repo.save_plan(plan_id, plan)


@app.task()
def complete_plans():
    logger.info("Running complete_plans")
    for plan_id in repo.plan_repo.get_all_plan_ids():
        plan = repo.plan_repo.get_plan_by_id(plan_id)
        tasks = repo.task_repo.get_tasks(plan_id)
        if plan.is_plan_running():
            if all_tasks_complete(tasks):
                    logger.info("Completing plan {}".format(plan_id))
                    plan.set_completed_on(utcnow_str())
                    plan.set_plan_as_complete()
                    repo.plan_repo.save_plan(plan_id, plan)
