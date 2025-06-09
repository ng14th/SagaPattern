
from fastapi import FastAPI
import os
import sys
from pathlib import Path


try:
    import core
except ModuleNotFoundError:
    current_path = Path(os.getcwd())
    sys.path.append(str(current_path))
    import core  # noqa


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.events import events
from core.middlewares.log_request import log_requests
from core.schema import ErrorResponseException
from core.schema.api_response import ApiResponse
from tortoise.transactions import atomic
from src.views import routers as routers_api

app = FastAPI(
    title="Auth-Zinc",
    on_startup=events,
)


@app.middleware("http")
@atomic(connection_name="master")
async def log_requests_middleware(request: Request, call_next):
    return await log_requests(request, call_next)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exception),
        },
    )


@app.exception_handler(ErrorResponseException)
async def error_response_exception_handler(request: Request, exception: ErrorResponseException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "success": exception.success,
            "data": exception.data,
            "message": exception.message,
            "count": exception.count,
            "error": exception.error,
            "error_code": exception.error_code,
            "status_code": exception.status_code
        },
    )


@app.get("/")
async def root():
    from core.context_var import event_id
    return {"message": f"Hello World {event_id.get_event_id()}"}


@app.get("/check-auth", response_model=ApiResponse)
async def check_auth(request: Request,):
    headers = request.headers
    custom_header = headers.get("X-Auth-User-Id")
    if custom_header != "user-test":
        raise ErrorResponseException(
            success=False,
            status_code=401,
            error_code=401,
            error="Unauthorized",
            message="Unauthorized",
        )

    return {"message": "Okie"}


for data_router in routers_api:

    router = data_router.get('router')
    prefix = data_router.get('prefix')  # /library

    prefix = f'/api{prefix}'
    app.include_router(router, prefix=prefix)
