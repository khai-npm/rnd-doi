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

class AdminOrderStatusDetailSchema(BaseModel):
    total_order_count : int
    active_order_count : int
    closed_order_count : int
    expired_order_count : int