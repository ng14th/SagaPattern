import ujson
import os
import sys
from pathlib import Path
from aio_pika import Message

try:
    import core
except ModuleNotFoundError:
    current_path = Path(os.getcwd())

    sys.path.append(str(current_path))
    import core  # noqa
    import src


from core.rabbitmq.async_consumer import AsyncRabbitMqConsumer
from core.async_redis.redis_lock_manager import redis_lock
from src.app.models import Inventory


class PaymentFailureConsummer(AsyncRabbitMqConsumer):

    async def rollback_inventory(self, inventory_id, quantity):
        lock = await redis_lock.create_lock('create_order_controller', timeout=3, inventory_id=inventory_id)
        async with lock:
            inventory = await Inventory.filter(id=inventory_id).first()
            if not inventory:
                self.logger.warning(f"Not found {inventory_id=}")
                return

            inventory.quantity = inventory.quantity + quantity
            await inventory.save(update_fields=["quantity"])
            self.logger.info(f"Rollback {inventory_id=} success")

    async def handle(self, message: Message):
        body = message.body
        if isinstance(body, bytes):
            body = ujson.loads(body)
        await self.rollback_inventory(body['inventory_id'], body['quantity'])
        return
