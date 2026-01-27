from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# changed * in password as %2A 
DATABASE_URL = "mysql+pymysql://showuser:Harish%2A1408@127.0.0.1:3306/showtracker2"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
