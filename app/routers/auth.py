from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

#in this path operation we go through how to login a user and the process behind it.

@router.post('/login', response_model=schemas.Token)
def login(user_info: OAuth2PasswordRequestForm = Depends(), db: session = Depends(database.get_db)):

    #we gotta remember that OAuth2PasswordRequestForm returns two fields with the names: 1)username and 2)password
    #so we can't say user_info.email.  because we don't have a field named email in OAuth2PasswordRequestForm.
    #we have to say OAuth2PasswordRequestForm.username.
    #this username can be anything. it can be email, id or whatever else.

    user = db.query(models.User).filter(models.User.email == user_info.username).first()

    if not user or not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"credentials are wrong!")

    #creating a JWT token, and remember data is the thing that we wanna put into the payload... we have added only id of the user
    # we can add any other piece of information about the user that we want...like role of the user or 
    #the scope of different endpoints that a user can access(because not all user have the same acceess level, 
    # admin has more access, also manager etc). we can add all of these information about a specific user in line below in data field.
    jwt_token = oauth2.create_access_token({'user_id':user.id})

    return {"jwt_token":jwt_token, "token_type":"bearer"}