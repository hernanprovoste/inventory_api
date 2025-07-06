from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.category import Category # Importamos el modelo de categoria del SQLAlchemy
from app.schemas.category import CategoryCreate, CategoryUpdate # Importamos los esquemas de categoria

# Obteneer una categoria por su ID
def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

# Obtener una categoria por nombre
def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()

# Obtener multiples categorias
def get_categories(db: Session, skip: int = 0, limit = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

# Crear una nueva categoria
def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit() # Esto permite guardar los cambios en la db
    db.refresh(db_category) # Actualiza la instancia con los datos generados por la DB.
    return db_category

# Actualizar una categoria existente
def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Optional[Category]:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        update_data = category.model_dump(exclude_unset=True) # Solo incluye los campos que fueron enviados
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    return db_category

# Eliminar una categoria
def delete_category(db: Session, category_id: int) -> Optional[Category]:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category