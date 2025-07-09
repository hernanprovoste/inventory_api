from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash
from app.models.user import User

# Test user registration
def test_register_user(client_for_testing: TestClient):
    response = client_for_testing.post(
        "/register",
        json={"email": "newuser@email.com", "password": "newpassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@email.com"
    assert "id" in data
    assert data["is_active"] is True
    assert data["is_admin"] is False

# Test to add an existng user
def test_register_existing_user(client_for_testing: TestClient):
    # Primero registramos uno
    client_for_testing.post(
        "/register",
        json={"email": "existing@example.com", "password": "password"}
    )
    # Intentamos registrar de nuevo con el mismo email
    response = client_for_testing.post(
        "/register",
        json={"email": "existing@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists."

# Test successful login
def test_login_for_access_token(db_session_for_testing: Session, client_for_testing: TestClient):
    # Creamos un usuario directamente en la DB de pruebas
    user_email = "login@example.com"
    user_password = "loginpassword"
    hashed_password = get_password_hash(user_password)
    db_user = User(email=user_email, hashed_password=hashed_password, is_active=True, is_admin=False)
    db_session_for_testing.add(db_user)
    db_session_for_testing.commit()

    response = client_for_testing.post(
        "/token",
        data={"username": user_email, "password": user_password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Test login with incorrect credentials
def test_login_incorrect_credentials(client_for_testing: TestClient):
    response = client_for_testing.post(
        "/token",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."