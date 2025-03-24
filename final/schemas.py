from datetime import date

from pydantic import BaseModel


class UserForm(BaseModel):
    name: str
    dob: date

class DeleteUserForm(BaseModel):
    confirm: bool