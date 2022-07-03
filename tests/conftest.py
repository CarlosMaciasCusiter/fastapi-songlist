from venv import create
import pytest
from app.config import settings
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_accesss_token
from app import models

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


@pytest.fixture
def test_user(client):
    user_data = {"email": "austincusiter1@gmail.com", "password": "password1234!"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_2(client):
    user_data = {"email": "austincusiter@gmail.com", "password": "password1234!"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_accesss_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_songs(test_user, test_user_2, session):
    songs_data = [
        {
            "title": "NEW MAGIC WAND",
            "artist": "Tyler The Creator",
            "single": False,
            "owner_id": test_user["id"],
        },
        {
            "title": "EARFQUAKE",
            "artist": "Tyler The Creator",
            "single": False,
            "owner_id": test_user["id"],
        },
        {
            "title": "RUNNING OUT OF TIME",
            "artist": "Tyler The Creator",
            "single": False,
            "owner_id": test_user["id"],
        },
        {
            "title": "RUNNING OUT OF TIME",
            "artist": "Tyler The Creator",
            "single": False,
            "owner_id": test_user_2["id"],
        },
    ]

    def create_song_model(song):
        return models.Songs(**song)

    songs_maps = map(create_song_model, songs_data)
    songs = list(songs_maps)
    session.add_all(songs)
    session.commit()
    songs = session.query(models.Songs).all()

    return songs
