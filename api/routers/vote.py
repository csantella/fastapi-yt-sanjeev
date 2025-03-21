from fastapi import status, HTTPException, Depends, APIRouter
import models
import oauth2
import schemas

from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Vote-System"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)
         ):
    
    # Check to see if the given post id exists before casting vote
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)

    if not post_query.first():
        # post does not exist
        raise(HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id '{vote.post_id}' does not exist"))
    found_vote = vote_query.first()
    if vote.direction == 1:
        # Check if vote already exits
        if found_vote:
            # User already voted
            raise(HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id '{current_user.id}' has already voted on post with id '{vote.post_id}'"))
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}
    
    else:
        if not found_vote:
            # Cannot delete vote that doesn't exst
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully removed vote"}
