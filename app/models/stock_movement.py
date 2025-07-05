from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base

class MovementType(str, enum.Enum):
    IN = "in"
    OUT = "out"

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Permitira agregrar que usuario hizo el movimiento

    product = relationship("Product", back_populates="stock_movements")
    #user = relationship("User", back_populates="stock_movements") 

    def __repr__(self):
        return f"<StockMovement(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, type={self.movement_type}, timestamp={self.timestamp})>"