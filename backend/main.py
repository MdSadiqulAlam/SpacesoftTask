from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dbconfig import SessionLocal, engine, Base
from models import User, UserReqModel, TodoModel, TodoReqModel

app = FastAPI()
Base.metadata.create_all(bind=engine)

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


@app.post("/create-user")
async def create_user(new_user: UserReqModel, db: db_dependency):
    user = User(name=new_user.name, email=new_user.email, password=new_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully!", "user_id": user.id}


@app.get("/users")
async def get_users(db: db_dependency):
    users = db.query(User).all()
    return users


@app.post("/create-todo")
async def create_todo(new_todo: TodoReqModel, db: db_dependency):
    todo = TodoModel(
        title=new_todo.title,
        description=new_todo.description,
        complete=new_todo.complete,
        owner_id=new_todo.owner_id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "Todo created successfully!", "todo_id": todo.id}


@app.get("/todos")
async def get_todos(db: db_dependency):
    todos = db.query(TodoModel).all()
    return todos


@app.get("/todos/{owner_id}")
async def get_todos_by_owner(owner_id: str, db: db_dependency):
    todos = db.query(TodoModel).filter(TodoModel.owner_id == owner_id).all()
    return todos


@app.put("/update-todo/{todo_id}")
async def update_todo(todo_id: int, updated_todo: TodoReqModel, db: db_dependency):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        return {"message": "Todo not found!"}

    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.complete = updated_todo.complete
    todo.owner_id = updated_todo.owner_id

    db.commit()
    db.refresh(todo)
    return {"message": "Todo updated successfully!", "todo_id": todo.id}


@app.delete("/delete-todo/{todo_id}")
async def delete_todo(todo_id: int, db: db_dependency):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        return {"message": "Todo not found!"}

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully!"}
