import pytest

from app.service import TaskService
from tests.fixtures.tasks.cache_repository import task_cache


@pytest.fixture
def task_service(task_cache, task_repository):
    return TaskService(task_cache=task_cache,
                       task_repository=task_repository)
