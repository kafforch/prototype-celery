from workers.base import app, repo


@app.task()
def store_new_plan(plan):
    with repo.lock_manager:
        plan_id = repo.plan_repo.save_new_plan(plan)
        repo.task_repo.save_new_tasks(plan_id, plan.get_tasks())
        repo.task_repo.save_dependencies(plan_id, plan.get_dependencies())
        return plan_id
