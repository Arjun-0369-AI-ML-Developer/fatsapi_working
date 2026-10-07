from fastapi import FastAPI
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base
from pydantic import BaseModel
from fastapi import Depends


app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer,primary_key=True)
    title = Column(String)
    complted = Column(String)

Base.metadata.create_all(bind= engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/home")
def home(db:Session = Depends(get_db)):
    return {
        "message": "DB connected fine"
    }