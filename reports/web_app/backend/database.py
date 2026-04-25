from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace these values with your PostgreSQL connection details.
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/medbot_db"

# Create engine. No special connect_args needed for PostgreSQL.
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models.
Base = declarative_base()

# User model.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
