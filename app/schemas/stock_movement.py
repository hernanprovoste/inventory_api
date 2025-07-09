from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum

from app.schemas.product import Product as ProductSchema

# Refinition Enum
class MovementType(str, enum.Enum):
    IN = "in"
    OUT = "out"

# Base schema for stock movements
class StockMovementBase(BaseModel):
    product_id: int = Field(..., description="Product ID to move")
    quantity: int = Field(..., gt=0, description="Quantity of product to move (must be greater than 0)")
    movement_type: MovementType = Field(..., description="Type of movement (in or out)")

class StockMovementCreate(StockMovementBase):
    pass

class StockMovement(StockMovementBase):
    id: int
    timestamp: datetime
    product: ProductSchema

    class Config:
        from_attributes = True