from beanie import Document, Indexed
from datetime import datetime
from pydantic import BaseModel


class Menu(Document):
    title: Indexed(str, unique=True) # type: ignore
    created_by : str
    link: str
    image_name: str

    class Settings:
        name = "menu"


class Item(BaseModel):
    item_detail_id : str
    created_by: str
    food_id : str
    order_for: str
    food: str
    price: int
    quantity: int
    note : str


class Order(Document):
    title: str
    status : str #= ({"active" : 1, "closed" : 2, "expired" : 3})
    created_by: str
    created_at : datetime
    description: str
    namesAllowed: list[str]
    menu: str
    area: int
    share: bool
    order_date: datetime
    item_list: list[Item]

    class Settings:
        name = "order"


class ItemOrder(Document):
    created_at : datetime
    created_by: str
    food_id : str
    order_id: str
    order_for: str
    food: str
    price : int
    quantity: int
    note : str

    class Settings:
        name = "item_detail"


class UserOrder(Document):
    username : Indexed(str, unique=True) # type: ignore
    allow_order_id_list: list[str]
    class Settings:
        name = "user_order"




