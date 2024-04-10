from datetime import datetime
from beanie import Document, Indexed


class User(Document):
    fullname: str
    email : str
    username: Indexed(str, unique=True) # type: ignore
    password: str
    role : str
    area : int
    join_date : datetime
    img_url : str

    class Settings:
        name = "users"
