

from core.async_redis.redis_lock_manager import redis_lock
from core.async_redis.client import RedisClient
from core.schema import ErrorResponseException
from src.app.schemas import *
from src.app.models import Inventory
from src.app.utils.rmq_client import OrderRabbitMqClient


redis_client: RedisClient = RedisClient()
order_client: OrderRabbitMqClient = OrderRabbitMqClient()


async def create_order_controller(body: OrderSchema):

    inventory_id = body.inventory_id
    quantity = body.quantity
    success = body.success

    lock = await redis_lock.create_lock('create_order_controller', timeout=3, inventory_id=inventory_id)
    async with lock:
        inventory = await Inventory.filter(id=inventory_id).first()
        if not inventory:
            raise ErrorResponseException(
                status_code=400,
                message=f"Không tìm thấy {inventory_id=}"
            )

        if inventory.quantity - quantity < 0:
            raise ErrorResponseException(
                status_code=400,
                message=f"Tồn kho không đủ {inventory_id=}"
            )

        inventory.quantity = inventory.quantity - quantity
        await inventory.save(update_fields=["quantity"])
        await order_client.publish_order_to_payment({
            "inventory_id": inventory_id,
            "quantity": quantity,
            "success": success
        })

    return "Hoàn tất đặt hàng -> Chuyển sang thanh toán"
