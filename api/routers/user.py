from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from database import engine, get_db
from sqlalchemy.orm import Session

import crud, models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password
    user.password = utils.hash(user.password)

    # create new user database entry
    new_user = models.User(**user.model_dump())

    # add new user object to the db
    db.add(new_user)

    # commit changes to db store
    db.commit()

    # replace 'new_user' with the refreshed version from the database
    db.refresh(new_user)

    return new_user


@router.get("/{id}",response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    # get user
    query_user = crud.get_user_by_id(db, id)

    if query_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found.")

    return query_user