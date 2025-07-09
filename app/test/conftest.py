# inventory_api/app/tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient # Para simular solicitudes HTTP
from unittest.mock import patch # Para "mockear" dependencias
from app.core.config import get_settings

from main import app# Importamos nuestra aplicación FastAPI
from app.db.database import get_db, Base # Importamos la dependencia de DB y la Base de SQLAlchemy
from app.core.config import get_settings # Para cargar la configuración
from app.models.user import User # Importamos el modelo User para crear un usuario de prueba
from app.core.security import get_password_hash # Para hashear la contraseña del usuario de prueba

settings = get_settings()

# Sobreescribir la configuración para usar la base de datos de pruebas
# Esto asegura que get_settings() devuelva la URL de la base de datos de pruebas.
@pytest.fixture(scope="session", autouse=True)
def test_settings_override():
    settings.TEST_DATABASE_URL = "sqlite:///./test.db" # Usamos un archivo SQLite para las pruebas, más fácil de inspeccionar si algo falla.
    # Alternativa para SQLite en memoria (más rápida pero no persistente): "sqlite:///:memory:"
    return settings

# Fixture para la base de datos de pruebas
@pytest.fixture(scope="function") # Scope "function" significa que se ejecuta para cada test
def db_session_for_testing():
    # Crea un motor SQLite en memoria para las pruebas
    engine = create_engine(get_settings().TEST_DATABASE_URL, echo=False)
    # Crea todas las tablas en la base de datos de pruebas
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db # Proporciona la sesión de DB al test
    finally:
        db.close()
        # Elimina las tablas después de cada test para asegurar un estado limpio
        Base.metadata.drop_all(bind=engine)

# Fixture para sobrescribir la dependencia get_db en la aplicación FastAPI
@pytest.fixture(scope="function")
def override_get_db(db_session_for_testing):
    def _override_get_db():
        yield db_session_for_testing
    app.dependency_overrides[get_db] = _override_get_db # Sobreescribe la dependencia global
    yield
    app.dependency_overrides.clear() # Limpia las sobreescrituras después del test

# Fixture para un cliente de prueba de FastAPI
@pytest.fixture(scope="function")
def client_for_testing(override_get_db):
    return TestClient(app)

# Fixture para crear un usuario de prueba y obtener su token (útil para tests de rutas protegidas)
@pytest.fixture(scope="function")
def test_user_and_token(db_session_for_testing, client_for_testing):
    db = db_session_for_testing
    user_email = "test@example.com"
    user_password = "testpassword"
    hashed_password = get_password_hash(user_password)

    test_user = User(
        email=user_email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    # Generar un token de acceso para este usuario de prueba
    # Necesitamos simular el endpoint /token o importar la función create_access_token directamente
    from app.core.security import create_access_token
    from datetime import timedelta
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": test_user.email}, expires_delta=access_token_expires)

    return {"user": test_user, "token": token}