from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.main import app

from app.config import settings
from app.database import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/test_database_fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    # run our code before we return our test
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overide_get_db
    yield TestClient(app)
    # run our code after the code finishes
