from typing import List

from dotenv import load_dotenv
load_dotenv()
import os 

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


admin_key = os.environ.get("ADMIN_KEY")
view_key = os.getenv('VIEW_KEY')

# Create user. This is for !verify endpoint
@app.post("/api/v1/auth/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if user.auth_token != admin_key:
        raise HTTPException(status_code= 403, detail= 'Access Denied')

    db_user = crud.get_user_by_id(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

# once monitor picks a change of owner. Deletes their info from API so they can't use bot
@app.delete("/api/v1/auth/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: str, user : schemas.authToken, db : Session = Depends(get_db)):

    if user.auth_token != admin_key:
        raise HTTPException(status_code= 403, detail= 'Access Denied')

    user_data = crud.get_user_by_id(db=db, id=user_id)

    if user_data:
        crud.delete_user_by_id(db = db, user= user_data)
        raise HTTPException(status_code=200, detail="User Successfully Deleted")
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# updates user data. For !reset and !key endpoints. Generates new key and clears session
@app.patch("/api/v1/auth/users/{user_id}", response_model = schemas.User)
def update_user(user_id : str, update_data : schemas.updateUser, db : Session = Depends(get_db)):

    if update_data.auth_token != admin_key:
        raise HTTPException(status_code= 403, detail= 'Access Denied')
    
    user_data = crud.get_user_by_id(db=db, id = user_id)

    if user_data:
        updated_user = crud.update_user(db = db, user= update_data, db_user = user_data)
        return updated_user
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Admin endpoint. View all users
@app.post("/api/v1/auth/users/view", response_model=List[schemas.User])
def read_all_users(user: schemas.authToken, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    if user.auth_token != admin_key:
        raise HTTPException(status_code= 403, detail= 'Access Denied')

    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Search user based of discord ID. This is for !info endpoint
@app.post("/api/v1/auth/user/search/id/{user_id}", response_model=schemas.User)
def search_user_id(user_id: str, user : schemas.authToken, db : Session = Depends(get_db)):

    if user.auth_token != admin_key and view_key:
        raise HTTPException(status_code= 403, detail= 'Access Denied')

    user_data = crud.get_user_by_id(db=db, id=user_id)

    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User Not Found")

# Searches your session based on key. Used for bot auth to check you + your session is valid.
@app.post("/api/v1/auth/user/search/key/{user_key}", response_model=schemas.User)
def search_user_key(user_key: str, user : schemas.authToken, db : Session = Depends(get_db)):

    if user.auth_token != admin_key:
        if user.auth_token != view_key:
            raise HTTPException(status_code= 403, detail= 'Access Denied')
    
    user_data = crud.get_user_by_key(db=db, key=user_key)

    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User Not Found")

# Searches for user based on mint. Response is sent to delete for delting user when owner of mint has changed
@app.post("/api/v1/auth/user/search/mint/{user_mint}", response_model=schemas.User)
def search_user_mint(user_mint: str, user : schemas.authToken, db : Session = Depends(get_db)):

    if user.auth_token != admin_key:
        raise HTTPException(status_code= 403, detail= 'Access Denied')
    
    user_data = crud.get_user_by_mint(db=db, mint=user_mint)

    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User Not Found")




