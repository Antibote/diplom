from datetime import datetime

from pydantic import BaseModel


class TaskForm(BaseModel):
    dob: datetime
    name: str
    task: str
    date_create: datetime
    who_cook: str
    who_comp: str
    result: bool


class DeleteTaskForm(BaseModel):
    confirm: bool
