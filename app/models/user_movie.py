from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class UserMovie(Base):
    __tablename__ = "user_movies"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    status = Column(String(20), nullable=False)  # watchlist, watching, completed
    created_at = Column(TIMESTAMP, server_default=func.now())
