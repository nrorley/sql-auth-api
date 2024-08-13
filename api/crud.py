from sqlalchemy.orm import Session

import models, schemas


def get_user_by_id(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_key(db: Session, key: str):
    return db.query(models.User).filter(models.User.key == key).first()

def get_user_by_mint(db: Session, mint: str):
    return db.query(models.User).filter(models.User.mint == mint).first()

def delete_user_by_id(db: Session, user: schemas.User):
    db.delete(user)
    db.commit()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    db_user = models.User(id = user.id, key = user.key, session = user.session, mint = user.mint)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.updateUser, db_user: schemas.User):

    if user.key:
        setattr(db_user, 'key', user.key)
        db.commit()
        db.refresh(db_user)
    if user.session:
        setattr(db_user, 'session', user.session)
        db.commit()
        db.refresh(db_user)

    return db_user