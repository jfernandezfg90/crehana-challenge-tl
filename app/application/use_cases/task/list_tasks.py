from typing import List, Optional
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.domain.value_objects.task_priority import TaskPriority
from app.domain.value_objects.task_status import TaskStatus


class ListTasksResult:
    def __init__(self, tasks: List[Task], total: int, completion_percentage: float):
        self.tasks = tasks
        self.total = total
        self.completion_percentage = completion_percentage


class ListTasksUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(
        self,
        task_list_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> ListTasksResult:
        all_tasks = self.task_repository.get_all_by_list(task_list_id)
        total_all = len(all_tasks)
        done_count = sum(1 for t in all_tasks if t.status == TaskStatus.DONE)
        completion_percentage = (
            round((done_count / total_all) * 100, 1) if total_all > 0 else 0.0
        )

        filtered_tasks = self.task_repository.get_all_by_list(
            task_list_id, status=status, priority=priority
        )

        return ListTasksResult(
            tasks=filtered_tasks,
            total=len(filtered_tasks),
            completion_percentage=completion_percentage,
        )
