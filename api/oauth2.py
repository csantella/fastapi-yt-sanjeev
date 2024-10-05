from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from database import get_db
from sqlalchemy.orm import Session

import crud, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET-KEY
# Algorithm
# Expiration time

SECRET_KEY = "cc0defbaba80f83dd8d870c924d11c1a4e56fcfab804934dbd2512411b2ba7e2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_id(db, id)
    
    if user is None:
        raise credentials_exception
    return user
