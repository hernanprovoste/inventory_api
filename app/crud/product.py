from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int) -> Optional[Product]:
    # Usamos joinedload para cargar la relacion 'category' de una vez (evita N+1 problem)
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str) -> Optional[Product]:
    return db.query(Product).filter(Product.name == name).first()

def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None, # Nuevo parametro para filtraar por categoria
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_stock: Optional[int] = None,
        max_stock: Optional[int] = None
) -> List[Product]:
    query = db.query(Product).options(joinedload(Product.category)) # Cargar la categoría para todos los productos

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if min_stock is not None:
        query = query.filter(Product.stock_quantity >= min_stock)
    if max_stock is not None:
        query = query.filter(Product.stock_quantity <= max_stock)

    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Recargar la relación de categoría después de refresh para asegurar que esté disponible
    # Esto es necesario si la relación no se carga automáticamente con refresh en algunos casos
    db_product = db.query(Product).options(joinedload(Product.category)).filter(Product.id == db_product.id).first()
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        db_product = db.query(Product).options(joinedload(Product.category)).filter(Product.id == db_product.id).first()
    return db_product

def delete_product(db: Session, product_id: int) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product