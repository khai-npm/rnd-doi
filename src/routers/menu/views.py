from typing import Annotated
from fastapi import APIRouter, Form, UploadFile, Depends, File, status
from src.schemas.response import ApiResponse
from src.schemas.order import (
    CreateMenuSchema,
    CreateOrderSchema,
    GetMenuImageSchema,
    GetFoodImageSchema,
    AddNewItemSchema,
    AddNewItemByOrderIDSchema,
    UpdateOrderStatusSchema
    
)
from src.schemas.admin import (
    AdminMenuDetailSchema,
    )
from src.schemas.food import food_schema, AddNewItemSchemaV3
from src.models.food import Food
from src.routers.menu.utils import (
    create_new_menu,
    create_new_order,
    get_order,
    get_order_v2,
    get_menu,
    get_image_of_menu,
    add_new_item_to_order,
    add_new_item_to_order_by_id,
    add_new_food,
    get_all_food,
    get_food_by_menu_title,
    add_new_item_v3,
    do_get_order_by_id,
    do_get_food_by_order_id,
    get_my_order,
    get_my_order_expired,
    get_order_created, get_order_joined,
    get_user_image_by_order_id,
    update_order_status,
    set_expired_order,
    do_delete_item_by_id,
    do_delete_order_by_id_v2,
    do_get_total_bill_order_by_order_id,
    do_get_food_bill_order_by_order_id,
    do_get_personal_bill_order_by_order_id_and_username,
    do_delete_food_by_id,
    do_delete_menu_by_title_v2,
    reverse_get_my_order,
    do_get_menu_detail_for_admin,
    do_update_menu_image_by_title,
    do_update_menu_info_by_title,
    add_image_to_food,
    do_get_overall_data_for_admin,
    do_get_total_bill_per_user_list
    # get_food_by_menu_from_order
)

from src.auth.auth_bearer import jwt_validator, get_current_user, get_current_area, jwt_validator_admin
from src.models.order import Menu, Order, Item

menu_router = APIRouter(prefix="/api/menu", tags=["Menu"])


@menu_router.post("/up_image", response_model=ApiResponse)
async def up_image(image: UploadFile = File(...)):
    from src.routers.menu.utils import upload_img_v1

    result = await upload_img_v1(image)
    return {"data": []}


@menu_router.post(
    "/create_menu", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def create_menu(
    request_data: CreateMenuSchema = Depends(CreateMenuSchema.as_form),
    # image: UploadFile = File(...),
    current_user:str = Depends(get_current_user)
):
    result = await create_new_menu(request_data, current_user)
    return {"data": [result]}

@menu_router.put(
    "/update_menu/image" , dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def update_menu_image(id : str = Form(...), image : UploadFile = File(...)):
    try:
        await do_update_menu_image_by_title(menu_id=id, image=image)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : []}

@menu_router.put(
    "/update_menu/" , dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def update_menu_by_id(id : str = Form(...), new_title : str = Form(...), new_link : str = Form(...)):
    try:
        await do_update_menu_info_by_title(menu_id=id, new_link=new_link, new_title=new_title)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : []}


@menu_router.post(
    "/create_order", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def create_order(request_data: CreateOrderSchema, current_user:str = Depends(get_current_user)):
    result = await create_new_order(request_data, current_user)
    return {"data": [result]}


@menu_router.post(
    "/get_all_order", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_all_order():
    await set_expired_order()
    result = await get_order()
    return {"data": result}

#-------------------[new get order]------------
@menu_router.post(
    "/get_user_order", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_order_by_user(current_user:str = Depends(get_current_user), current_area: int = Depends(get_current_area)):
    await set_expired_order()
    result = await get_order_v2(current_user, current_area)
    return {"data": result}
#----------------------------------------------

#-------------------[new get order]------------
@menu_router.post(
    "/get_user_order/not_joined", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_order_by_user(current_user:str = Depends(get_current_user), current_area: int = Depends(get_current_area)):
    await set_expired_order()
    result = await reverse_get_my_order(current_user, current_area)
    return {"data": result}
#----------------------------------------------


#---------------------[get order user by id]------------------
@menu_router.get(
    "/get_user_order/{order_id}", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_order_by_id(order_id : str):
    await set_expired_order()
    result =  await do_get_order_by_id(order_id)
    return {"data" : [result]}
#-------------------------------------------------------------


#---------------------[get foods by order id]------------------
@menu_router.get(
    "/get_user_order/{order_id}/foods", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_food_by_order_id(order_id : str):
    result =  await do_get_food_by_order_id(order_id)
    return {"data" : result}
#-------------------------------------------------------------

#--------------[get my order]--------------------
@menu_router.get(
        "/get_my_order/all", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def routing_get_my_order(current_user:str = Depends(get_current_user)):
    await set_expired_order()
    result = await get_my_order(current_user)
    return {"data" : result}
#------------------------------------------------

#--------------[get my order - History]--------------------
@menu_router.get(
        "/get_my_order/history", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def routing_get_my_order_history(current_user:str = Depends(get_current_user)):
    await set_expired_order()
    result = await get_my_order_expired(current_user)
    return {"data" : result}
#------------------------------------------------

#--------------[get my order - created by  / joined filter]----------
@menu_router.get(
        "/get_my_order/created", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def routing_get_my_order_created(current_user:str = Depends(get_current_user)):
    await set_expired_order()
    result = await get_order_created(current_user)
    return {"data" : result}

@menu_router.get(
        "/get_my_order/joined", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def routing__get_my_order_joined(current_user:str = Depends(get_current_user)):
    await set_expired_order()
    result = await get_order_joined(current_user)
    return {"data" : result}
#------------------------------------------------------


@menu_router.post(
    "/get_all_menu", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_all_menu():
    result = await get_menu()
    return {"data": result}


@menu_router.post(
    "/get_menu_image", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_menu_image(request_data: GetMenuImageSchema):
    result = await get_image_of_menu(request_data.image_name)
    return {"data": [result]}


@menu_router.post(
    "/add_new_item_old_v2", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def add_new_item(request_data: AddNewItemByOrderIDSchema, current_user:str = Depends(get_current_user)):
    await set_expired_order()
    result = await add_new_item_to_order_by_id(request_data, current_user)
    return {"data": [result]}

@menu_router.post(
    "/add_new_item_old_v1", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def add_new_item(request_data: AddNewItemSchema):
    await set_expired_order()
    result = await add_new_item_to_order(request_data)
    return {"data": [result]}

@menu_router.delete(
    "/delete_menu/{id}", dependencies=[Depends(jwt_validator_admin)],response_model=ApiResponse
)
async def delete_menu_by_title(id: str, current_user:str = Depends(get_current_user)): 
    try:

        await do_delete_menu_by_title_v2(id, current_user)

    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : []}


@menu_router.delete(
    "/delete_order_v1/{title}",
    dependencies=[Depends(jwt_validator)],
    status_code=status.HTTP_200_OK,
)
async def delete_order_by_title(title: str) -> dict:
    order = await Order.find_one({"title": title})
    if order is not None:
        await order.delete()
        return order.model_dump()
#--------------------[delete order by id - v2]----------------------    
@menu_router.delete(
    "/delete_order/{order_id}",
    dependencies=[Depends(jwt_validator)],
     response_model=ApiResponse
)
async def delete_order_by_id(order_id: str, current_user:str = Depends(get_current_user)):
    try:
        await do_delete_order_by_id_v2(order_id, current_user)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : []}
#-------------------------------------------------------------------- 

#--------------------[delete food by id - v2]----------------------    
@menu_router.delete(
    "/delete_food/{food_id}",
    dependencies=[Depends(jwt_validator_admin)],
     response_model=ApiResponse
)
async def delete_food_by_id(food_id: str):
    try:
        await do_delete_food_by_id(food_id)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : []}
#--------------------------------------------------------------------   

@menu_router.delete(
    "/delete_item/{item_id}",
    dependencies=[Depends(jwt_validator)],
     response_model=ApiResponse,
)
async def delete_item_by_id(item_id: str, current_user:str = Depends(get_current_user)):
        try:

            await do_delete_item_by_id(item_id=item_id, current_user=current_user)

        except Exception as e:
            return {"success" : False, "error" : str(e)}
        
        return {"data" : []}
    

@menu_router.get(
        "/get_user_order/{order_id}/user_image", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def routing_get_user_image_by_order_id(order_id : str):
    try:
        result = await get_user_image_by_order_id(order_id)

    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data": [result]}

@menu_router.put(
        "/update_order/status/", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def routing_update_order_status(request_data : UpdateOrderStatusSchema, current_user:str = Depends(get_current_user)):
    try:
        result = await update_order_status(request_data, current_user)

    except Exception as e:
        return {"success" : False, "error" : str(e)}
    return {"data" : [result]}


#-------------------------[NEW FOOD MENU UPDATE]-------------------
@menu_router.post(
    "/add_new_food",
    dependencies=[Depends(jwt_validator_admin)],
    response_model=ApiResponse
)

async def add_food_by_menu(request_data: food_schema = Depends(food_schema.as_form),
                        #    image: UploadFile = File(...),
                           current_user:str = Depends(get_current_user)):
    result = await add_new_food(request_data, current_user)

    return {"data" : [result]}

@menu_router.put(
    "/add_new_food/image",
    dependencies=[Depends(jwt_validator_admin)],
    response_model=ApiResponse
)

async def add_food_by_menu(food_id : str = Form(...), image : UploadFile = File(...)):
    result = await add_image_to_food(food_id, image)

    return {"data" : [result]}


@menu_router.post("/get_all_food", dependencies=[Depends(jwt_validator)])
async def get_food():
    result = await get_all_food()

    return {"data" : result}



@menu_router.post("/get_food_by_menu", dependencies=[Depends(jwt_validator)])
async def get_food(menu_title : str):
    result = await get_food_by_menu_title(menu_title)

    return {"data" : result}


@menu_router.post("/add_new_item", dependencies=[Depends(jwt_validator)], response_model=ApiResponse)
async def add_food(request_data : AddNewItemSchemaV3, current_user:str = Depends(get_current_user)):
    await set_expired_order()
    result = await add_new_item_v3(current_user, request_data)

    return {"data" : [result]}


@menu_router.post("/get_food_image", dependencies=[Depends(jwt_validator)], response_model=ApiResponse)
async def show_food_image(request_data : GetFoodImageSchema):
    result = await get_image_of_menu(request_data.image_url)
    return {"data": [result]}
#-------------------------------------------------------------------

#-------------------------------[GET PAYMENT INFOMATION UPDATE]-----------------------------------

@menu_router.get(
    "/get_user_order/{order_id}/bill/total", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_total_bill_order_by_order_id(order_id : str):
    try:
        result = await do_get_total_bill_order_by_order_id(order_id)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : [result]}


@menu_router.get(
    "/get_user_order/{order_id}/bill/food", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_food_bill_order_by_order_id(order_id : str):
    try:
        result = await do_get_food_bill_order_by_order_id(order_id)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : [result]}

@menu_router.get(
    "/get_user_order/{order_id}/bill/user", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_total_bill_per_user_list(order_id: str):
    try:
        result = await do_get_total_bill_per_user_list(order_id)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : result}

@menu_router.get(
    "/get_user_order/{order_id}/bill/{username}", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_personal_bill_order_by_order_id_and_username(order_id : str, username : str):
    try:
        result = await do_get_personal_bill_order_by_order_id_and_username(order_id, username)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : [result]}

@menu_router.get(
    "/get_user_order/{order_id}/bill/me", dependencies=[Depends(jwt_validator)], response_model=ApiResponse
)
async def get_personal_bill_order_by_order_id_and_username(order_id : str, current_user:str = Depends(get_current_user)):
    try:
        result = await do_get_personal_bill_order_by_order_id_and_username(order_id, current_user)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : [result]}



#---------------------------------------------------------------------------------------------------


#---------------------------------[Admin Only Dashboard function update]--------------------------------
# @menu_router.get(
#     "/admin/menu_detail", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
# )
# async def get_menu_detail_admin():
#     try:

#         result = await do_get_menu_detail_for_admin()
    
#     except Exception as e:
#         return {"success" : False, "error" : str(e)}
    
#     return {"data" : result}

# @menu_router.get(
#     "/admin/overall_detail", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
# )
# async def get_data_admin():
#     try:

#         result = await do_get_overall_data_for_admin()
    
#     except Exception as e:
#         return {"success" : False, "error" : str(e)}
    
#     return {"data" : [result]}
#-------------------------------------------------------------------------------------------------------
    


