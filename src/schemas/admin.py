from pydantic import BaseModel

class AdminMenuDetailSchema(BaseModel):
    menu_title : str
    order_count : int
    food_count : int

class AdminOverallDataSchema(BaseModel):
    user_count : int
    menu_count : int
    order_count : int
    food_count : int
