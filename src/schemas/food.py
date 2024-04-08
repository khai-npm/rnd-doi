from fastapi import Form
from pydantic import BaseModel
class food_schema(BaseModel):
    food_name : str
    price: int
    ingredients : list = []
    menu_title : str

    @classmethod
    def as_form(cls, food_name: str = Form(...), 
                price: int = Form(...), 
                ingredients: list[str] = Form(...), 
                menu_title: str = Form(...)):
        
        return cls(food_name=food_name, 
                   price=price, 
                   ingredients=ingredients, 
                   menu_title=menu_title)

class ItemV3(BaseModel):
    order_for : str
    food_id : str
    quantity : int
    note: str

class AddNewItemSchemaV3(BaseModel):
    order_id : str
    new_items: list[ItemV3]