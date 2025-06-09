import asyncio
from src.consumer.worker_order import OrderWorker

if __name__ == '__main__':
    worker: OrderWorker = OrderWorker()
    asyncio.run(worker.run())
