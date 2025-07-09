from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.category import Category as CategorySchema

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., ge=0) # Ge significa mayor o igual a 0
    stock_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., description="ID de la categoria a la que pertenece el producto")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0) # Valida que sea un valor flotante y mayor o igual a 0
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = Field(None, description="ID de la categoria a la que pertenece el producto")

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Muesta la categoria completa al obtener un producto
    category: CategorySchema

    class Config:
        from_attributes = True