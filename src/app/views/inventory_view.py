from fastapi import APIRouter, BackgroundTasks, Request
from core.schema.api_response import ApiResponse
from src.app.schemas import CreateInventory, OrderSchema
from src.app.controllers.order_controller import create_order_controller

router = APIRouter(tags=["inventory"])


@router.post('', response_model=ApiResponse)
async def order(
    request: Request,
    body: OrderSchema
):
    message = await create_order_controller(body)
    return {"message": message}
