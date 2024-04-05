from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.exceptions.error_response_exception import ErrorResponseException
from src.constants.error_code import get_error_code
from src.exceptions.error_response_exception import ErrorResponseException
from src.exceptions.exception_handler import (
    error_response_handler,
    request_validation_error_handler,
)
from src.routers.menu.views import menu_router
from src.routers.users.views import user_router
from src.routers.menu.admin_views import admin_router
from src.events.startup import events as startup_events
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(on_startup=startup_events)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ErrorResponseException, error_response_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)

app.include_router(admin_router)
app.include_router(menu_router)
app.include_router(user_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}
