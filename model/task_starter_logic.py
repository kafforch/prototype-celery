def get_tasks_available_to_start(plan_id, tasks, dependencies):

    def is_task_not_complete(task_id):
        task = filter(lambda t: t.get_task_id() == task_id, tasks)[0]
        return not task.is_task_complete()

    def outstanding_dependencies_for_task(task, dependencies):
        preceding_task_ids = map(lambda d1: d1.get_from(),
                                 filter(lambda d2: d2.get_to() == task.get_task_id(), dependencies)
                                 )
        return filter(is_task_not_complete, preceding_task_ids)

    def is_task_ready_to_start(task):
        if task.is_task_initial():
            return len(outstanding_dependencies_for_task(task, dependencies)) == 0
        else:
            return False

    return filter(is_task_ready_to_start, tasks)
