from sqlalchemy.orm import Session

import models


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()