# Add new user
@route.post("/users")
def add_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Retrieve a list of all users
@route.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Retrieve details for a specific user
@route.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Update an existing user
@route.put("/users/{user_id}")
def update_user(user_id: int, request: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for key, value in request.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return {"message": "User updated successfully"}
    return {"error": "User not found"}

# Delete an existing user
@route.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"error": "User not found"}