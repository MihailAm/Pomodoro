from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository, TaskCache
from schema import TaskCreateSchema
from schema.task import TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self):
        cached_tasks = self.task_cache.get_tasks()
        if cached_tasks:
            return cached_tasks

        tasks = self.task_repository.get_tasks()
        task_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(task_schema)
        return task_schema

    def create_task(self, body: TaskCreateSchema, user_id: int):
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return TaskSchema.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)


    def delete_task(self,task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)