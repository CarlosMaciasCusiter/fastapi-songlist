from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.get("/", response_model=List[schemas.SongOut])
def get_songs(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    # SQLalchemy performs by default left inner join
    results = (
        db.query(models.Songs, func.count(models.Vote.song_id).label("votes"))
        .join(models.Vote, models.Vote.song_id == models.Songs.id, isouter=True)
        .group_by(models.Songs.id)
        .filter(models.Songs.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Song)
def create_songs(
    song: schemas.SongCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_song = models.Songs(owner_id=current_user.id, **song.dict())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@router.get("/{id}", response_model=schemas.SongOut)
def get_song(
    id: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    song = (
        db.query(models.Songs, func.count(models.Vote.song_id).label("votes"))
        .join(models.Vote, models.Vote.song_id == models.Songs.id, isouter=True)
        .group_by(models.Songs.id)
        .filter(models.Songs.id == id)
        .first()
    )
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"song with id: {id} was not found",
        )
    return song


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    song_query = db.query(models.Songs).filter(models.Songs.id == id)
    song = song_query.first()
    if song == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"song with id: {id} was not found",
        )
    if song.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to delete"
        )
    song_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Song)
def update_song(
    id: int,
    updated_song: schemas.SongCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    song_query = db.query(models.Songs).filter(models.Songs.id == id)
    song = song_query.first()
    if song == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"song with id: {id} was not found",
        )
    if song.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to update"
        )
    song_query.update(updated_song.dict(), synchronize_session=False)
    db.commit()
    return song_query.first()
