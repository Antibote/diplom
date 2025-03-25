from datetime import date

from pydantic import BaseModel


class TaskForm(BaseModel):
    dob: date
    name: str
    task: str
    date_create: date
    who_cook: str
    who_comp: str
    result: bool


class DeleteTaskForm(BaseModel):
    confirm: bool
