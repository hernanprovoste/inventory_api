from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db # Esto importa la istancia de la DB
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.crud import category as crud_category # Alias para generar las operaciones CRUD

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db) # Se inyecta la sesion de la base de datos
):
    db_category = crud_category.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category exist in database with this name."
        )
    return crud_category.create_category(db=db, category=category)

@router.get("/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud_category.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )
    return db_category

@router.put("/{category_id}", response_model=Category)
def update_existing_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = crud_category.update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found to update."
        )
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found to delete."
        )
    return {"message": "Category deleted successfully"}