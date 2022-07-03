import pytest
from app import models


@pytest.fixture()
def test_vote(test_songs, session, test_user):
    new_vote = models.Vote(song_id=test_songs[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_song(authorized_client, test_songs):
    res = authorized_client.post(
        "/votes/", json={"song_id": test_songs[0].id, "dir": 1}
    )
    assert res.status_code == 201


def test_vote_twice(authorized_client, test_songs, test_vote):
    res = authorized_client.post(
        "/votes/", json={"song_id": test_songs[3].id, "dir": 1}
    )
    assert res.status_code == 409


def delete_vote(authorized_client, test_songs, test_vote):
    res = authorized_client.song(
        "/votes/", json={"song_id": test_songs[3].id, "dir": 1}
    )
    assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_songs):
    res = authorized_client.post(
        "/votes/", json={"song_id": test_songs[3].id, "dir": 0}
    )
    assert res.status_code == 404


def test_vote_song_not_exist(authorized_client, test_songs):
    res = authorized_client.post("/votes/", json={"song_id": 80000, "dir": 0})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_songs):
    res = client.post("/votes/", json={"song_id": test_songs[3].id, "dir": 0})
    assert res.status_code == 401
