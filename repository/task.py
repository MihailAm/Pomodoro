from dataclasses import dataclass

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models import Tasks, Categories
from schema import TaskCreateSchema
from schema.task import TaskSchema


@dataclass
class TaskRepository:
    db_session: AsyncSession

    async def get_tasks(self):
        async with self.db_session as session:
            result = await session.execute(select(Tasks))
            task: list[Tasks] = list(result.scalars().all())
        return task

    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task: Tasks = (await session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(name=task.name,
                           pomodoro_count=task.pomodoro_count,
                           category_id=task.category_id,
                           user_id=user_id)
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            return task_model.id

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)

        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_task_by_cat_name(self, cat_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == cat_name)
        async with self.db_session as session:
            result = await session.execute(query)
            task: list[Tasks] = list(result.scalars().all())
        return task

    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task
