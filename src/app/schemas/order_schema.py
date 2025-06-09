from pydantic import BaseModel
from pydantic import BaseModel, field_validator


class OrderSchema(BaseModel):
    inventory_id: int
    quantity: int
    success: bool

    @field_validator('quantity')
    def validate_quantity(cls, value):
        if value <= 0:
            raise 'quantity must be > 0'
        return value


class CreateInventory(BaseModel):
    inventory_id: int
    name: str
    quantity: int
    price: int

    @field_validator('quantity')
    def validate_quantity(cls, value):
        if value <= 0:
            raise 'quantity must be > 0'
        return value

    @field_validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise 'price must be > 0'
        return value
