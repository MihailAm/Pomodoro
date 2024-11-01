from unittest.mock import AsyncMock

import pytest

from app.exception import TaskNotFound
from app.service import TaskService


async def test_get_tasks_with_cache(task_service: TaskService):
    tasks = await task_service.get_tasks()

    assert len(tasks) != 0
    for task in tasks:
        assert isinstance(task.id, int)
        assert isinstance(task.name, str)
        assert isinstance(task.pomodoro_count, int)
        assert isinstance(task.category_id, int)
        assert isinstance(task.user_id, int)


async def test_get_tasks_without_cache(task_service: TaskService):
    task_service.task_cache = AsyncMock()
    task_service.task_cache.get_tasks.return_value = None

    tasks = await task_service.get_tasks()

    assert len(tasks) != 0
    for task in tasks:
        assert isinstance(task.id, int)
        assert isinstance(task.name, str)
        assert isinstance(task.pomodoro_count, int)
        assert isinstance(task.category_id, int)
        assert isinstance(task.user_id, int)


async def test_update_task_name_not_found_task(task_service: TaskService):
    with pytest.raises(TaskNotFound):
        await task_service.update_task_name(task_id=1, name="test_task", user_id=1)
