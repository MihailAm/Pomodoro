import pytest
import asyncio

pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.settings",
    "tests.fixtures.users.user_model",
    "tests.fixtures.tasks.cache_repository",
    "tests.fixtures.tasks.task_service",
    "tests.fixtures.tasks.task_repository"
]

