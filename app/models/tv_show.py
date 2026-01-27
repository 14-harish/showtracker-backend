from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class TVShow(Base):
    __tablename__ = "tv_shows"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_tv_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    first_air_year = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    poster_path = Column(String(255))