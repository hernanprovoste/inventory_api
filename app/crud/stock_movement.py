from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.models.stock_movement import StockMovement, MovementType
from app.models.product import Product
from app.schemas.stock_movement import StockMovementCreate

from fastapi import HTTPException, status

# Get movements by ID
def get_stock_movement(db: Session, stock_movement_id: int) -> Optional[StockMovement]:
    return db.query(StockMovement).options(joinedload(StockMovement.product)).filter(StockMovement.id == stock_movement_id).first()

# Get multiple stock moviments with filters options and pagination
def get_stock_movements(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        product_id: Optional[int] = None,
        movement_type: Optional[MovementType] = None # Filter by movement type
) -> List[StockMovement]:
    query = db.query(StockMovement).options(joinedload(StockMovement.product))
    if product_id is not None:
        query = query.filter(StockMovement.product_id == product_id)
    if movement_type is not None:
        query = query.filter(StockMovement.movement_type == movement_type)
    return query.offset(skip).limit(limit).all()

# Create new stock movement and update product stock
def create_stock_movement(db: Session, movement: StockMovementCreate) -> StockMovement:
    # Get product to move
    db_product = db.query(Product).filter(Product.id == movement.product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product ID {movement.product_id} not found."
        )

    # Calculate new stock
    if movement.movement_type == MovementType.IN:
        db_product.stock_quantity += movement.quantity
    elif movement.movement_type == MovementType.OUT:
        if db_product.stock_quantity < movement.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product ID {movement.product_id} has not enough stock quantity to move {movement.quantity}."
            )
        db_product.stock_quantity -= movement.quantity
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid movement type {movement.movement_type}."
        )

    # Add record of stock movement
    db_movement = StockMovement(
        product_id=movement.product_id,
        movement_type=movement.movement_type,
        quantity=movement.quantity
    )

    # Add and commit changes in both tables
    db.add(db_product)
    db.add(db_movement)
    db.commit()
    db.refresh(db_product)
    db.refresh(db_movement)

    # Reload relationship of product to movement
    db_movement = db.query(StockMovement).options(joinedload(StockMovement.product)).filter(StockMovement.id == db_movement.id).first()
    return db_movement
