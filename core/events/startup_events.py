from core.constants import AUTH_CONSOLE
from core.database.db_postgresql import db_init
from core.format_log.init_logger import create_console_logger
from core.async_redis.client import RedisClient
from core.async_redis.redis_lock_manager import redis_lock
from core.settings.service_setting import settings
from src.app.utils.rmq_client import OrderRabbitMqClient


async def startup_event_init_logger():
    create_console_logger(AUTH_CONSOLE)


async def startup_event_init_db():
    await db_init()


async def startup_event_init_redis():
    client: RedisClient = RedisClient()
    redis_client = await client.connect(settings.get_redis_server_url())
    redis_lock.set_redis_client(redis_client)


async def startup_event_init_rabbitmq_client():
    client: OrderRabbitMqClient = OrderRabbitMqClient()
    await client.connect(settings.get_rabbitmq_brokers())

events = [v for k, v in locals().items() if k.startswith('startup_event_')]
