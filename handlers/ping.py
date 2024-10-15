from typing import Union

from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/ping", tags=["ping-app, ping-db"])


@router.get("/db")
async def ping_db():
    return {"messsage": "ok"}


@router.get("/app")
async def ping_app():
    return {"messsage": "ok"}
