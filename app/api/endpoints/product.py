from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud import product as crud_product
from app.crud import category as crud_category # Necesario para validar category_id

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    # Validar que la categoria exista
    db_category = crud_category.get_category(db, category_id=product.category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with ID {product.category_id} does not exist."
        )

    # Validad que noe exista un producto con el mismo nombre
    db_product = crud_product.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product exist in database with this name."
        )

    return crud_product.create_product(db=db, product=product)

@router.get("/", response_model=List[Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    min_price: Optional[float] = Query(None, description="Filter by minimum price"),
    max_price: Optional[float] = Query(None, description="Filter by maximum price"),
    min_stock: Optional[int] = Query(None, description="Filter by minimum stock quantity"),
    max_stock: Optional[int] = Query(None, description="Filter by maximum stock quantity")
):
    products = crud_product.get_products(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        min_stock=min_stock,
        max_stock=max_stock
    )
    return products

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_existing_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    if product.category_id is not None:
        db_category = crud_category.get_category(db, category_id=product.category_id)
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with ID {product.category_id} does not exist."
            )

    db_product = crud_product.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found to update."
        )
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found to delete."
        )
    return {"message": "Product deleted successfully"}