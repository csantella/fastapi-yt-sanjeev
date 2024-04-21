from sqlalchemy.orm import Session, Query

import models


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def post_query_by_id(db: Session, id: int) -> Query:
    return db.query(models.Post).filter(models.Post.id == id)


def get_post_by_id(db: Session, id: int) -> models.Post:
    return post_query_by_id(db, id).first()
