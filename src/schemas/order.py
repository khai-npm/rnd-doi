from pydantic import BaseModel, field_validator
from fastapi import Form
from datetime import datetime
from src.exceptions.error_response_exception import ErrorResponseException
from src.constants.error_code import get_error_code


class CreateMenuSchema(BaseModel):
    title: str
    link: str

    @classmethod
    def as_form(cls, title: str = Form(...), link: str = Form(...)):
        return cls(title=title, link=link)


class CreateItemSchema(BaseModel):
    item_detail_id : str
    created_by : str
    order_for: str
    food_id : str
    food: str
    price: int
    quantity: int
    note : str


class CreateOrderSchema(BaseModel):
    title: str
    description: str
    namesAllowed: list[str]
    menu: str
    area: int
    # share: bool
    # item_list: list[CreateItemSchema]
    tags: list[str]
    order_date: str

    @field_validator("area")
    def validate_area(cls, v: int):
        if v != 1 and v != 2:
            raise ErrorResponseException(**get_error_code(4000103))
        return v

    # @field_validator("item_list")
    # def validate_item_list(cls, v: list[CreateItemSchema]):
    #     if len(v) == 0:
    #         raise ErrorResponseException(**get_error_code(4000104))
    #     return v


class GetMenuImageSchema(BaseModel):
    image_name: str

class GetFoodImageSchema(BaseModel):
    image_url: str


class AddNewItemSchema(BaseModel):
    new_item: list[CreateItemSchema]
    order: CreateOrderSchema


class AddNewItemByOrderIDSchema(BaseModel):
    order_id: str
    new_item: list[CreateItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    order_id : str

#-----------------------------------
class BillDetailSchema(BaseModel):
    username : str
    foodname : str
    quantity : int
    final_price : int

class TotalBillSchema(BaseModel):
    info : list[BillDetailSchema]
    total_price : int
#-----------------------------------
class FoodDetailSchema(BaseModel):
    food_name : str
    price : int
    quantity : int
    note: list[str]
    final_price : int

class TotalFoodSchema(BaseModel):
    info : list[FoodDetailSchema]
    total_price : int

    

