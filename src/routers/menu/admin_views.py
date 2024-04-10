
from fastapi import APIRouter, Depends, Form

from src.auth.auth_bearer import jwt_validator_admin
from src.models.users import User
from src.routers.menu.utils import (
    do_admin_reset_password,
    do_get_menu_detail_for_admin,
    do_get_overall_data_for_admin,
    do_get_overall_order_count,
    get_all_food,
    get_menu
)
from src.schemas.response import ApiResponse
from src.schemas.users import AllUserResponseSchema


admin_router = APIRouter(prefix="/api/admin", tags=["Admin"])

@admin_router.get(
    "/menu_statistic", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def get_menu_detail_admin():
    try:

        result = await do_get_menu_detail_for_admin()
    
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : result}

@admin_router.get(
    "/overall_statistic", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def get_data_admin():
    try:

        result = await do_get_overall_data_for_admin()
    
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : [result]}

@admin_router.get(
    "/order_statistic", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def get_order_data_admim():
    try:

        result = await do_get_overall_order_count()
    
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    return {"data" : [result]}

@admin_router.get(
    "/get_all_user", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def get_all_user():
    result = User.find_all()


    return_data = []
    async for data in result:
        return_data.append(AllUserResponseSchema(fullname=data.fullname,
                                                 username=data.username,
                                                 area=data.area,
                                                 role=data.role,
                                                 img_url=data.img_url))

    return {"data": return_data}


@admin_router.get("/get_all_food", dependencies=[Depends(jwt_validator_admin)])
async def get_food():
    result = await get_all_food()

    return {"data" : result}

@admin_router.get(
    "/get_all_menu", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def get_all_menu():
    result = await get_menu()
    return {"data": result}

@admin_router.put(
    "/reset_password", dependencies=[Depends(jwt_validator_admin)], response_model=ApiResponse
)
async def admin_reset_password(username : str = Form(...)):
    try:
        await do_admin_reset_password(username)
    except Exception as e:
        return {"success" : False, "error" : str(e)}
    
    return {"data" : []}
