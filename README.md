# ShowTracker Backend

Backend service for the ShowTracker application.

## Tech Stack
- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication
- TMDB API

## Features
- User authentication
- Movie and TV show tracking
- Watchlist / Watching / Completed status
- User dashboard
- TMDB integration

## Setup

 1. Clone repository

git clone https://github.com/14-harish/showtracker-backend.git
cd showtracker-backend


2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Environment variables
DATABASE_URL=mysql+pymysql://user:password@localhost/showtracker
TMDB_API_KEY=your_tmdb_api_key
JWT_SECRET=your_secret_key

5. Run server
uvicorn app.main:app --reload

Server runs at:
http://127.0.0.1:8000

API docs:
http://127.0.0.1:8000/docs

Commit it:

git add README.md
git commit -m "Add backend README"
git push
