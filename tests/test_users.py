import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from app.database import Base, get_db
from app.main import app
from app import schemas
from app.config import settings



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # reset the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    

def test_root(client):
    res = client.get('/')
    print(res.json())
    assert res.json().get('message') == 'Welcome To My Api!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json={"email": "aj123@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'aj123@gmail.com'