from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Annotated
import os

router = APIRouter(
    prefix="/notification",
    tags=["通知"]
)


def write_notification(email: str, message: str):
    with open("log.txt", "w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


def write_log(message: str):
    path = os.path.join(os.getcwd(), "app/notification/log.txt")
    with open(path, "a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f'found query: {q}\n'
        background_tasks.add_task(write_log, message)
    return q


@router.post("/send-notification/{email}")
async def send_notification(
        email: str,
        background_tasks: BackgroundTasks,
):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "消息正在发送中"}


@router.post("/new-send-notification/{email}")
async def new_send_notification(
        email: str,
        background_tasks: BackgroundTasks,
        q: Annotated[str, Depends(get_query)]
):
    message = f'message to {email}\n'
    background_tasks.add_task(write_log, email)
    return {"message": "消息发送了！"}
