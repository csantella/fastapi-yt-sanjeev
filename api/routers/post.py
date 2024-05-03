from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from database import get_db
from sqlalchemy.orm import Session

import crud, models, oauth2, schemas


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/")
async def get_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate,
                      db: Session = Depends(get_db),
                      user: models.User = Depends(oauth2.get_current_user)):
    """ INSERT INTO posts (title, content, published) 
            VALUES (%s, %s, %s) RETURNING *,
            (post.title, post.content, post.published))"""
    
    new_post = models.Post(**post.model_dump())
    
    # add new post object to the db
    db.add(new_post)

    # commit changes to db store
    db.commit()

    # replace 'new_post' with the refreshed version from the database
    db.refresh(new_post)

    return new_post
    

@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    # """SELECT * FROM posts WHERE id = %s""", (id,))
    query_post = crud.get_post_by_id(db, id)

    if query_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")

    return query_post
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # """DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    del_post = crud.post_query_by_id(db, id)

    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable to delete post with id:{id}. Post was not found.")
    
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}")
async def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s RETURNING *,
        (post.title, post.content, post.published, id))"""
    upd_query = crud.post_query_by_id(db, id)

    if upd_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} was not found.")
    
    upd_query.update(post.model_dump(),
                     synchronize_session=False)
    db.commit()
    return upd_query.first()