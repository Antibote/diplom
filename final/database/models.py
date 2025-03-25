from datetime import datetime
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    dob: datetime
    name: str
    task: str
    date_create: datetime
    who_cook: str
    who_comp: str
    result: str


