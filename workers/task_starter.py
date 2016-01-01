from workers.base import app, repo
from celery.utils.log import get_task_logger
from celery.schedules import timedelta
from model.task_starter_logic import get_tasks_available_to_start

START_TASKS_TASK_NAME = '{}.start_tasks'.format(__name__)

logger = get_task_logger(__name__)

app.conf.CELERYBEAT_SCHEDULE.update(
        dict(
                start_tasks=dict(
                        task=START_TASKS_TASK_NAME,
                        schedule=timedelta(seconds=repo.config.get_task_starter_cycle_time())
                )
        )
)


@app.task()
def start_tasks():
    for plan_id in repo.plan_repo.get_all_plan_ids():
        plan = repo.plan_repo.get_plan_by_id(plan_id)
        if plan.is_plan_running():
            with repo.lock_manager:
                dependencies = repo.task_repo.get_dependencies(plan_id)
                tasks = repo.task_repo.get_tasks(plan_id)
                available_tasks = get_tasks_available_to_start(plan_id, tasks, dependencies)
                logger.info("Tasks to start for plan {0}: {1}".format(
                    plan_id,
                    ", ".join(map(lambda t: t.get_task_id(), available_tasks))
                ))
