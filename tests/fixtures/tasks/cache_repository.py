import pytest

from app.schema import TaskSchema
from tests.fixtures.tasks.task_model import TasksFactory


class FakeCacheRepository:
    async def get_tasks(self) -> list[TaskSchema]:
        mock_tasks = [TasksFactory() for _ in range(5)]
        tasks = [TaskSchema.model_validate(task) for task in mock_tasks]
        return tasks

@pytest.fixture
def task_cache():
    return FakeCacheRepository()