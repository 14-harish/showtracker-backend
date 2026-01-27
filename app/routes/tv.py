from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.dependencies import get_current_user
from app.models.tv_show import TVShow
from app.models.user_tv_show import UserTVShow
from app.schemas.tv import TVSave

router = APIRouter(prefix="/tv", tags=["tv"])


@router.post("/save")
def save_tv_show(
    tv_in: TVSave,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # --- status validation ---
    if tv_in.status == "watching":
        if tv_in.current_season is None or tv_in.current_episode is None:
            raise HTTPException(
                status_code=400,
                detail="Watching requires current_season and current_episode"
            )

    if tv_in.status not in {"watchlist", "watching", "completed"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    # --- ensure TV show exists ---
    tv = db.query(TVShow).filter(
        TVShow.tmdb_tv_id == tv_in.tmdb_tv_id
    ).first()

    if not tv:
        tv = TVShow(
            tmdb_tv_id=tv_in.tmdb_tv_id,
            name=tv_in.name,
            first_air_year=tv_in.first_air_year,
            poster_path=tv_in.poster_path
        )
        db.add(tv)
        db.commit()
        db.refresh(tv)

    # --- prevent duplicates ---
    existing = db.query(UserTVShow).filter(
        UserTVShow.user_id == current_user.id,
        UserTVShow.tv_show_id == tv.id
    ).first()

    if existing:
        existing.status = tv_in.status
        existing.current_season = tv_in.current_season
        existing.current_episode = tv_in.current_episode
        existing.poster_path = tv_in.poster_path

        db.commit()
        return {"message": "TV show updated successfully"}

    # --- save user progress ---
    user_tv = UserTVShow(
        user_id=current_user.id,
        tv_show_id=tv.id,
        status=tv_in.status,
        current_season=tv_in.current_season,
        current_episode=tv_in.current_episode
    )

    db.add(user_tv)
    db.commit()

    return {"message": "TV show saved successfully"}
 
@router.delete("/{tmdb_tv_id}")
def remove_tv_show(
    tmdb_tv_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tv = db.query(TVShow).filter(
        TVShow.tmdb_tv_id == tmdb_tv_id
    ).first()

    if not tv:
        raise HTTPException(status_code=404, detail="TV show not found")

    user_tv = db.query(UserTVShow).filter(
        UserTVShow.user_id == current_user.id,
        UserTVShow.tv_show_id == tv.id
    ).first()

    if not user_tv:
        raise HTTPException(status_code=404, detail="TV show not in your list")

    db.delete(user_tv)
    db.commit()

    return {"message": "TV show removed"}