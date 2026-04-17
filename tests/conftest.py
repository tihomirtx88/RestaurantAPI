import uuid

import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models import *

# Creating test evnvirement
@pytest.fixture
def app():
   app = create_app("testing")

   app.config.update({
       "TESTING": True,
       "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
       "JWT_SECRET_KEY": "test-secret"
   })

   with app.app_context():
       db.create_all()
       yield app
       db.drop_all()

# -------------------------
# CLIENT FIXTURE
# -------------------------
@pytest.fixture
# simulate HTTPS requests
def client(app):
    return app.test_client()

# -------------------------
# TEST USER
# -------------------------
# Creating user
@pytest.fixture
def test_user(app):
    user = User(
        email=f"admin_{uuid.uuid4()}@admin.com",  # ← FIX
        role="admin"
    )
    user.set_password("123456")

    db.session.add(user)
    db.session.commit()

    return user

# -------------------------
# AUTH TOKEN
# -------------------------
@pytest.fixture
# Login user and takes token
def auth_token(client, test_user):
    response = client.post("/api/auth/login", json={
          "email": test_user.email,
        "password": "123456"
    })

    print("LOGIN:", response.status_code, response.get_json())

    return response.get_json()["access_token"]