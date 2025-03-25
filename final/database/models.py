from datetime import date
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    dob: date
    name: str
    task: str
    date_create: date
    who_cook: str
    who_comp: str
    result: str


