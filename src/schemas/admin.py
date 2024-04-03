from pydantic import BaseModel

class AdminMenuDetailSchema(BaseModel):
    menu_title : str
    order_count : int
    food_count : int
