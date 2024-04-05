
from fastapi import APIRouter, Depends

from src.auth.auth_bearer import jwt_validator_admin
from src.routers.menu.utils import (
    do_get_menu_detail_for_admin,
    do_get_overall_data_for_admin,
    do_get_overall_order_count
)
from src.schemas.response import ApiResponse


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
    
