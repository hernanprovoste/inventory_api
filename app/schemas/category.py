from pydantic import BaseModel, Field
from typing import Optional

# Esquema base para crear una nueva categoria
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100) # El ... indica que es un camporequerido
    description: Optional[str] = Field(None, max_length=500) # El Optional[str] indica que es un campo opcional o None por defecto

# Esquema para la creacion de una categoria (hereda de CategoryBase)
class CategoryCreate(CategoryBase):
    pass # No se agrega nada adicional, solo hereda de CategoryBase

# Esquema para la actualizacion de una categoria (todos los campos aqui son opcionales)
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

# Esquema para la respuesta de la API (lo que se devuelve al cliente)
# Incluye el ID y la relacion de productos
class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True # Esto permite que los campos de la base de datos se mapeen a los campos de la clase