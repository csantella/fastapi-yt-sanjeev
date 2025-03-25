from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
# from datetime import datetime, timezone
from sqlalchemy.orm import Session
import models
import oauth2
import schemas
import utils

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query_user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    # check if user exists or if the passwords match
    if not query_user or not utils.verify_passwd(user_cred.password, query_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    # create a token
    access_token = oauth2.create_access_token(
        data={"user_id": query_user.id})

    return {"access_token": access_token, "token_type": "bearer" }
