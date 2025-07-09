from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

# Load configuration and url database
settings = get_settings()

# Create engine and session maker
# Update logic to use producction database or testing database
DATABASE_URL_TO_USE = settings.DATABASE_URL_TEST if settings.TEST_DATABASE_URL else settings.DATABASE_URL
engine = create_engine(DATABASE_URL_TO_USE, echo=False) # Change echo to True in prod
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

# Modelos importados
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.stock_movement import StockMovement

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
