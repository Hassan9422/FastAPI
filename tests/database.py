import json
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine, true
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest


# the reason that we aadd this chuck of code here(from line ... to ) is that we wanna create a seperate instance of our database
# and we don't want to mix it with our developmenr instance of our database. we can call it testing instance of our database.
##################################################################################################
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port} /{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# we need line below for creating tables. without that, we are going to have a database without any table!
# Base.metadata.create_all(bind=engine)

####################################################################################################

# client = TestClient(app)

# the reasom that we have created this fixture below is that we wanna make our login_user test case independent from other
# other test cases. and alos we don't wanna make changes to the scope of our fixtures. also in this way it's not reliant on 
# any specific order in our test cases code. 
@pytest.fixture
def test_user(client):
    user_data = {"email":"h13@gmail.com", 'password':'940202'}
    res = client.post('/users/', json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def session():
    # run line below before our code excecutes. we wanna drop all existed tables, before doing anything. so we can start clean
    Base.metadata.drop_all(bind=engine)
    # run line below after our code excecuted, it's going to create all tables using sqlalchemy
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # Now here we rae basically saying that we wanna create a new seperate instance of our postgres database by overriding the old
    # instance of our databse which was 'get_db' in our development environment. so in this way we are going to create a new instance
    # of databse for the testing purposes.
    # whem we run line below, it's going to swap get_db in development environment and replace it with 'override_get_db'
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)