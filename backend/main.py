from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dbconfig import SessionLocal, engine, Base

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


def get_db():
    db = SessionLocal()
    try:
        # print("Opening DB session")
        yield db
    finally:
        # print("Closing DB session")
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


Base.metadata.create_all(bind=engine)
@app.get("/")
async def read_root():
    
    return {"message": "Hello from backend!"}


@app.get("/test-db")
async def test_db(db: db_dependency):
    return {"message": "Database connection successful!"}
