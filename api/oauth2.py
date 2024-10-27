from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from config import settings
from database import get_db
from models import User
from sqlalchemy.orm import Session

import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET-KEY
# Algorithm
# Expiration time


def create_access_token(data: dict, expires_delta: int = settings.access_token_expire_minutes):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, key=settings.secret_key, algorithm=settings.token_algorithm)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token=token, key=settings.secret_key, algorithms=settings.token_algorithm)
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == id).first()
    
    if user is None:
        raise credentials_exception
    return user
