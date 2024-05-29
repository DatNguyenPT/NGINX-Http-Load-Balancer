from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///admin_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'Admin'
    username = Column(String, unique=True, primary_key=True, nullable=False)
    password = Column(String, nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
