from celery.contrib.methods import task
import logging


class PlanSubmitter:

    def __init__(self, plan_repo, task_repo):
        self.__plan_repo = plan_repo
        self.__task_repo = task_repo

    @task()
    def store_plan(self, plan):
        plan_id = self.__plan_repo.save(plan)
        logger = logging.getLogger(__name__)
        logger.debug("Saving plan with id:{}".format(plan_id))
        self.__task_repo.save_tasks(plan_id, plan.get_tasks())
        self.__task_repo.save_dependencies(plan_id, plan.get_dependencies())
        return plan_id
