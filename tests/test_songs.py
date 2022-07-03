import pytest
from app import schemas


def test_get_all_songs(authorized_client, test_songs):
    res = authorized_client.get("/songs/")

    def validate(song):
        return schemas.SongOut(**song)

    songs_map = map(validate, res.json())
    songs_list = list(songs_map)

    assert len(res.json()) == len(test_songs)
    assert res.status_code == 200


def test_unauthorized_user_get_all_songs(client, test_songs):
    res = client.get("/songs/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_songs(client, test_songs):
    res = client.get(f"/songs/{test_songs[0].id}")
    assert res.status_code == 401


def test_get_one_song_not_exist(authorized_client, test_songs):
    res = authorized_client.get(f"/songs/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_songs):
    res = authorized_client.get(f"/songs/{test_songs[0].id}")
    song = schemas.SongOut(**res.json())
    assert song.Songs.id == test_songs[0].id
    assert song.Songs.title == test_songs[0].title


@pytest.mark.parametrize(
    "title, artist, single",
    [
        ("Humble", "Kendrick Lamar", True),
        ("Alright", "Kendrick Lamar", False),
        ("United In Grief", "Kendrick Lamar", False),
    ],
)
def test_create_song(authorized_client, test_user, test_songs, title, artist, single):
    res = authorized_client.post(
        "/songs/", json={"title": title, "artist": artist, "single": single}
    )
    created_song = schemas.Song(**res.json())
    assert res.status_code == 201
    assert created_song.title == title
    assert created_song.artist == artist
    assert created_song.single == single
    assert created_song.owner_id == test_user["id"]


def test_create_song_default_single_true(authorized_client, test_user, test_songs):
    res = authorized_client.post(
        "/songs/",
        json={
            "title": "arbritrary title",
            "artist": "some artist",
        },
    )
    created_song = schemas.Song(**res.json())
    assert res.status_code == 201
    assert created_song.title == "arbritrary title"
    assert created_song.artist == "some artist"
    assert created_song.single == False
    assert created_song.owner_id == test_user["id"]


def test_unauthorized_user_create_song(client, test_user, test_songs):
    res = client.post(
        "/songs/",
        json={
            "title": "arbritrary title",
            "artist": "some artist",
        },
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_song(client, test_user, test_songs):
    res = client.delete(
        f"/songs/{test_songs[0].id}",
    )
    assert res.status_code == 401


def test_delete_song_success(authorized_client, test_user, test_songs):
    res = authorized_client.delete(
        f"/songs/{test_songs[0].id}",
    )
    assert res.status_code == 204


def delete_song_not_exist(authorized_client, test_user, test_songs):
    res = authorized_client.delete(
        f"/songs/{test_songs[1232121].id}",
    )
    assert res.status_code == 404


def test_delete_other_users_songs(authorized_client, test_user, test_songs):
    res = authorized_client.delete(
        f"/songs/{test_songs[3].id}",
    )
    assert res.status_code == 403


def test_update_song(authorized_client, test_user, test_songs):
    data = {"title": "updated song", "artist": "updated artist", "id": test_songs[0].id}
    res = authorized_client.put(f"/songs/{test_songs[0].id}", json=data)
    updated_song = schemas.Song(**res.json())
    assert res.status_code == 200
    assert updated_song.title == data["title"]
    assert updated_song.artist == data["artist"]


def test_update_other_user_song(authorized_client, test_user, test_user_2, test_songs):
    data = {"title": "updated song", "artist": "updated artist", "id": test_songs[3].id}
    res = authorized_client.put(f"/songs/{test_songs[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_song(client, test_songs):
    res = client.delete(f"/songs/{test_songs[3].id}")
    assert res.status_code == 401


def test_update_song_does_not_exist(authorized_client, test_user, test_songs):
    data = {"title": "updated song", "artist": "updated artist", "id": test_songs[0].id}
    res = authorized_client.put(f"/songs/548920", json=data)
    assert res.status_code == 404
