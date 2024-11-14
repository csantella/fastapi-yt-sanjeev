from fastapi import Response, status, HTTPException, Depends, APIRouter
import models, oauth2, schemas
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
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.direction == 1:
        # Check if vote already exits
        if found_vote:
            # User already voted
            raise(HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post with id:{vote.post_id}"))
        
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