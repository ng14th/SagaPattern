import os
import sys
from pathlib import Path
from aio_pika import Message
import ujson


try:
    import core
except ModuleNotFoundError:
    current_path = Path(os.getcwd())

    sys.path.append(str(current_path))
    import core  # noqa
from core import constants
from core.rabbitmq.async_consumer import AsyncRabbitMqConsumer
from core.abstractions.singeton import Singleton


class PaymentConsummer(AsyncRabbitMqConsumer):

    def _singleton_init(self, **kwargs):
        return super()._singleton_init(**kwargs)

    async def handle(self, message: Message, **kwargs):
        body = message.body
        if isinstance(body, bytes):
            body = ujson.loads(body)

        self.logger.info("from inventory", body)
        if body.get('success'):
            self.logger.info("Payment Success")
        else:
            self.logger.warning("Payment Failed")
            self.logger.info(
                f"Publish to payment failure to {constants.ORDER_PAYMENT_FAILURE_QUEUE} to rollback"
            )

            await self._publish(
                body,
                constants.ORDER_EXCHANGE,
                constants.ORDER_PAYMENT_FAILURE_ROUTING_KEY
            )

        return
