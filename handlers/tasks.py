from typing import Annotated

from fastapi import FastAPI, APIRouter, status, Depends, HTTPException

from dependecy import get_tasks_repository, get_task_service, get_request_user_id
from exception import TaskNotFound
from repository import TaskRepository
from schema import TaskSchema, TaskCreateSchema
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_task_service)]):
    task = await task_service.get_tasks()
    return task


@router.post("/", response_model=TaskSchema)
async def create_task(body: TaskCreateSchema,
                      task_service: Annotated[TaskService, Depends(get_task_service)],
                      user_id: int = Depends(get_request_user_id)):
    task = await task_service.create_task(body, user_id)

    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def patch_task(task_id: int,
                     name: str,
                     task_service: Annotated[TaskService, Depends(get_task_service)],
                     user_id: int = Depends(get_request_user_id)):
    try:
        update_task = await task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
        return update_task
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete("/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int,
                      task_service: Annotated[TaskService, Depends(get_task_service)],
                      user_id: int = Depends(get_request_user_id)):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
