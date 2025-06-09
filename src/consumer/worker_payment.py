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
from .payment_consumer import PaymentConsummer


class PaymentWorker(AsyncRabbitMqConsumer):
    async def run(self, **kwargs):
        try:
            await super().setup(settings)
            await self.setup()
        except KeyboardInterrupt:
            self.logger.info('bye bye')

    async def setup_payment_consumer(self, class_handler=PaymentConsummer):
        queue = await self.create_queue(
            exchange_name=constants.PAYMENT_EXCHANGE,
            exchange_type=rabbit.ExchangeType.DIRECT,
            queue_name=constants.PAYMENT_QUEUE,
            routing_key=constants.PAYMENT_ROUTING_KEY,
            rabbitmq_urls=settings.get_rabbitmq_brokers()
        )
        handler: PaymentConsummer = class_handler()
        handler.broker = self.broker
        await self.consume(queue, handler.handle)

    async def setup(self):
        list_coros = [
            self.setup_payment_consumer(),
        ]
        await asyncio.gather(*list_coros)
        await asyncio.Future()
