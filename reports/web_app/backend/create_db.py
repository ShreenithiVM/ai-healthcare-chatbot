# backend/create_db.py
from database import engine, Base

def create_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()
