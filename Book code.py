from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, get_db
from sqlalchemy import Column, Integer, String, ForeignKey
import schemas, models


route = APIRouter()


# Add new user
@route.post("/users", response_model=schemas.User)
def add_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
                           id=request.id,
                           name=request.name,
                           birthday=request.birthday,
                           gender=request.gender,
                           email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Retrieve a list of all users
@route.get("/users", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# Retrieve details for a specific user
@route.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update an existing user
@route.put("/users/{user_id}")
def update_user(user_id: int, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in request.dict().items():
        setattr(user, key, value)
    db.commit()
    return {"message": "User updated successfully"}


# Delete an existing user
@route.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
