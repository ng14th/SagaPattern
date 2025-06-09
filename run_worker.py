import asyncio
from src.consumer.worker_payment import PaymentWorker

if __name__ == '__main__':
    worker: PaymentWorker = PaymentWorker()
    asyncio.run(worker.run())
