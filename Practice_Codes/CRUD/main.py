from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from fastapi.responses import JSONResponse

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None

users : Dict[int, User] = {}

@app.post("/users/")
def create_user(user: User):
    if user.id in users:
        raise HTTPException(400, "User already present")
    users[user.id] = user
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(404, "User is not present")
    return users[user_id]

@app.put("/users/{user_id}")
def update_email(user_id: int, email: EmailStr):
    if user_id not in users:
        raise HTTPException(404, "User not present in database")
    user = users[user_id]
    user.email = email
    users[user_id] = user
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(404, "User not present in database")
    del users[user_id]
    return JSONResponse(status_code=200, content={"message" : "User deleted successfully"})
