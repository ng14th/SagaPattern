import os
import sys
from pathlib import Path


try:
    import core
except ModuleNotFoundError:
    current_path = Path(os.getcwd())

    sys.path.append(str(current_path))
    import core  # noqa

import asyncio
from core.rabbitmq.async_consumer import AsyncRabbitMqConsumer
from core.settings.service_setting import settings
from core import constants
from faststream import rabbit
from .payment_failure_consumer import PaymentFailureConsummer


class OrderWorker(AsyncRabbitMqConsumer):
    async def run(self, **kwargs):
        try:
            await super().setup(settings)
            await self.setup()

        except KeyboardInterrupt:
            self.logger.info('bye bye')

    async def setup_order_payment_failure_consumer(self, class_handler=PaymentFailureConsummer):
        queue = await self.create_queue(
            exchange_name=constants.ORDER_EXCHANGE,
            exchange_type=rabbit.ExchangeType.DIRECT,
            queue_name=constants.ORDER_PAYMENT_FAILURE_QUEUE,
            routing_key=constants.ORDER_PAYMENT_FAILURE_ROUTING_KEY,
            rabbitmq_urls=settings.get_rabbitmq_brokers()
        )
        handler: PaymentFailureConsummer = class_handler()
        handler.broker = self.broker
        await self.consume(queue, handler.handle)

    async def setup(self):
        list_coros = [
            self.setup_order_payment_failure_consumer()
        ]
        await asyncio.gather(*list_coros)
        await asyncio.Future()
