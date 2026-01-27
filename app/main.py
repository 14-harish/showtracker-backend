from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.routes.users import router as users_router
from app.models.movie import Movie
from app.models.user_movie import UserMovie
from app.routes.movies import router as movies_router
from app.routes.tmdb import router as tmdb_router
from app.models.tv_show import TVShow
from app.models.user_tv_show import UserTVShow
from app.routes.tv import router as tv_router
from app.routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(movies_router)
app.include_router(tmdb_router)
app.include_router(tv_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "ShowTracker backend is running"}



