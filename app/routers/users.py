from sqlalchemy.orm import Session
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas
from app import utils
from ..database import engine, get_db


router = APIRouter(
    prefix='/users', tags=['Users']
)

# in below path operation, user is an pydantic object that stores the email and password of the user. 
# and db is an object that we need to make a session to our databse.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response_User)
#since we're gonna interact with the database, we have to use db object as a parameter to function below.
def Create_A_User(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #this below lines of code is how we can save something to the database after we created it
    #but before doing anything we gotta hash the password and save it into the database instead of the real password.
    hashed_password = utils.hash(user.password)
    #updating pydantic user model after hashing the password and replacing the original password with the hashed one
    user.password = hashed_password
    #adding and saving inforamation into the databse
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


@router.get("/{id}", response_model=schemas.Response_User)
def get_user(id: int,db: Session = Depends(get_db)):
    desired_user = db.query(models.User).filter(models.User.id == id).first()

    if not desired_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id={id} does not exist")

    return desired_user