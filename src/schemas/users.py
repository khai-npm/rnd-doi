from fastapi import Form
from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    fullname: str
    username: str
    area: int
    password: str
    confirm_password : str


class UpdateUserSchema(BaseModel):
    fullname : str
    area : int
    @classmethod
    def as_form(cls, fullname: str = Form(...), area: str = Form(...)):
        return cls(fullname=fullname, area=area)

class UpdatePasswordSchema(BaseModel):
    old_password : str
    new_password : str
    confirm_password : str

class AllUserResponseSchema(BaseModel):
    fullname : str
    username : str
    area : int
    role : str
    img_url : str
