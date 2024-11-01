from dataclasses import dataclass

import pytest

from app.schema import TaskSchema
from tests.fixtures.tasks.task_model import TasksFactory


@dataclass
class FakeTaskRepository:
    async def get_tasks(self):
        mock_tasks = [TasksFactory() for _ in range(5)]
        return mock_tasks

    async def get_user_task(self, user_id: int, task_id: int):
        return None


@pytest.fixture
def task_repository():
    return FakeTaskRepository()
