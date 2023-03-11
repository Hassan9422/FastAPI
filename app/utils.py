from passlib.context import CryptContext


#defining hashing algorithm in code below
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

