from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey("categories.id"))

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacion para vincular productos con categorias
    category = relationship("Category", back_populates="products")

    # Relacion para vincular productos con movimientos de stock
    stock_movements = relationship("StockMovement", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"