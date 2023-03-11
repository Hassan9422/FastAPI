from datetime import datetime, timedelta
from telnetlib import STATUS
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
# if we wanna fetch the users from the database we have to import database library 
from . import schemas, database, models
from sqlalchemy.orm import session
from .config import settings


auth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#in this file we are going to create our jwt token. we need threee things: 1)secret key, 2)algorithm type and 3)expiration time
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


#the access token can have a payload, data is the payload that we wanna encode into the token
def create_access_token(payload_data:dict):
    #because we don't wanna change the oroginal data, we are going to make a copy of the original data

    copied_payload_data = payload_data.copy()
    # now we are going to create expiration field in our token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # now we add the expiration field into the payload data that we wanna encode in our jwt token
    copied_payload_data.update({'exp':expire})
    # now we can create the jwt token using three pieces of data: payload data(copied_data), secret key and algorithm_type.
    CREATED_JWT_TOKEN = jwt.encode(copied_payload_data, SECRET_KEY, algorithm=ALGORITHM)
    return CREATED_JWT_TOKEN
  
#in the function below, we are gonna verify that the tojen is still valid. 
# so if the user go agead and change something in the token, it is going to return us an error. 
# or it can be also because of something else that has went wrong in the token, so we return an error.
def verify_jwt_token(token:str, credential_exception):
    
    try:
        #here we wanna extract the payload data from the token, so we use decode method.if the token is not valid, it can't decode it
        # and it will give us an error
        payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #here we wanna make sure that we have an id field in our payload and we wanna get it
        id: str = payload_data.get("user_id")
        #making sure that id is available and correct
        if not id:
            raise credential_exception
        #validating schema for our whole token data, which in this casse it is only id. but it can be a list of properties
        # not necessarily one.  actually we wanna make sure that it matched the specific schema we have defined for it
        token_data = schemas.tokenData(id=id)
    
    #and finally counting for unconsidered errors
    except JWTError:
        raise credential_exception

    #and finally we are going to the whole token_data which in our case is just only id of the user.
    return token_data

# so we can give this below function to any of our path operations to make them protetected. what it means is that 
# for  example we can pass this below function to createpost endponit function to take the jwt token from the request automatically,
#  extract the id and it also is going to verify that token is valid by calling verify token function inside of auth.py file. 
# because crating a post needs the user to be logged in. so we have to add this below function 
# as a dependency to that specific path operation that we wanna protect

#  one other idea behind below function is that once the verify function returns token_data which is the id of the user,
#  below function can fetch the user from the database based on the id. and then we can attach the user to any
#  path operation to perform any necessary logic with that. but in this specific example here till now 
#  we haven't fetched the user in function below to do anything with that, but we can absolutely do that in the future.
#  so it's up to you to how to fetch the user from the database. you can also fetch the user from the database inside of path operation
#  themselves. because they have id of the user, they can fetch the user based on the id themselves.
#  or instead of that, as I said you can fetch the user here in below function automatically instead on in path operations.
#  so the point is that you don't have to fetch the user here, you can also fetch it in any path operation you like.

#in order to get access to the database object and send a request to it,we have to pass session dependency into below function: 

def get_current_user(token: str = Depends(auth2_scheme), db: session = Depends(database.get_db)):
    #defining the credentials_exception
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized!'
    , headers={"WWW-Authenticate":"Bearer"})

    # again please remember that token in below line is nothing but id of the user, because it equals to the return value of 
    # verify function which is token_data which itself is just id of the user.
    token = verify_jwt_token(token, credential_exception)
    # now we can grab the user here based on the id, if we want
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user



