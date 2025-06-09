from src.app.views import (
    inventory_router
)

routers = [
    {"router": inventory_router, "prefix": "/order"}
]
