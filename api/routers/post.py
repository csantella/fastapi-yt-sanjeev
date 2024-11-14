from typing import Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from database import get_db
from sqlalchemy.orm import Session

import models, oauth2, schemas


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db),
                    curr_user: int = Depends(oauth2.get_current_user),
                    limit: int = 25,
                    skip: int = 0,
                    search: Optional[str] = ""
                    ):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate,
                      curr_user: models.User = Depends(oauth2.get_current_user),
                      db: Session = Depends(get_db)):
    
    new_post = models.Post(owner_id=curr_user.id, **post.model_dump())
    
    # add new post object to the db
    db.add(new_post)

    # commit changes to db store
    db.commit()

    # replace 'new_post' with the refreshed version from the database
    db.refresh(new_post)

    return new_post
    

@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int,
                   curr_user: int = Depends(oauth2.get_current_user),
                   db: Session = Depends(get_db)):
    query_post = db.query(models.Post).filter(models.Post.id == id).first()

    if query_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")

    return query_post
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,
                      curr_user: int = Depends(oauth2.get_current_user),
                      db: Session = Depends(get_db)):
    del_query = db.query(models.Post).filter(models.Post.id == id)
    del_post = del_query.first()

    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable to delete post with id:{id}. Post was not found.")
    
    if curr_user.id != del_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Unable to delete post with id:{id}. User '{curr_user.email}' is not authorized to perform the delete action on this post.") 
    
    del_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}")
async def update_post(post: schemas.PostUpdate,
                      id: int,
                      curr_user: int = Depends(oauth2.get_current_user),
                      db: Session = Depends(get_db)):
    """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s RETURNING *,
        (post.title, post.content, post.published, id))"""
    upd_query = db.query(models.Post).filter(models.Post.id == id)
    upd_post = upd_query.first()

    if upd_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} was not found.")
    
    if curr_user.id != upd_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Unable to update post with id:{id}. User '{curr_user.email}' is not authorized to perform the update action on this post.") 
    
    upd_query.update(post.model_dump(),
                     synchronize_session=False)
    db.commit()
    return upd_query.first()