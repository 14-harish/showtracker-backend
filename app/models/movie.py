from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_movie_id = Column(Integer, unique=True, nullable=False)
    title = Column(String(150), nullable=False)
    release_year = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    poster_path = Column(String(255))
