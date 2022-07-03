import pytest
from app import schemas
from jose import jwt
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("Hello"))
#     assert res.json().get("Hello") == "World!!"


def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "austincusiter@gmail.com", "password": "password1234"},
    )
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "austincusiter@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert res.status_code == 200
    assert login_res.token_type == "bearer"
    assert id == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("austincusiter@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password1234", 422),
        ("austincusiter@gmail.com", None, 422),
    ],
)
def test_failed_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
