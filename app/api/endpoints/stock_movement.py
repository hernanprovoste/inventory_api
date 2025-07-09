from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.stock_movement import StockMovement, StockMovementCreate, MovementType
from app.crud import stock_movement as crud_stock_movement
from app.crud import product as crud_product

router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"]
)

@router.post("/", response_model=StockMovement, status_code=status.HTTP_201_CREATED)
def create_new_stock_movement(movement: StockMovementCreate, db: Session = Depends(get_db)):
    return crud_stock_movement.create_stock_movement(db=db, movement=movement)

@router.get("/", response_model=List[StockMovement])
def read_stock_movements(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        product_id: Optional[int] = Query(None, description="Filter by product ID"),
        movement_type: Optional[MovementType] = Query(None, description="Filter by movement type")
):
    movements = crud_stock_movement.get_stock_movements(
        db,
        skip=skip,
        limit=limit,
        product_id=product_id,
        movement_type=movement_type
    )
    return movements

@router.get("/{stock_movement_id}", response_model=StockMovement)
def read_stock_movement(stock_movement_id: int, db: Session = Depends(get_db)):
    db_movement = crud_stock_movement.get_stock_movement(db, stock_movement_id=stock_movement_id)
    if db_movement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock movement not found."
        )
    return db_movement