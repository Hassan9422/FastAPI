# in this file, we're gonna make sure that our environemnt variables have a correct schema, so we wanna validate them.

from pydantic import BaseSettings


class Settings(BaseSettings):
    # these are our environemnt variables that we need for this project. there could be even 50 or more of them if it's needed.
    database_hostname: str
    database_port: str
    database_password: str
    database_name:str
    database_username:str
    secret_key:str
    algorithm: str
    access_token_expire_minutes: int

    # by adding this class below, we are telling pydantic to look at .env file in this directory to import all values for our 
    # environment variables.
    class Config:
        env_file = ".env"


# creating an instance of the class above
settings = Settings()

