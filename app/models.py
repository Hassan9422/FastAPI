import email
from sqlalchemy import INTEGER, Column, ForeignKey, String, Integer, Boolean, TIMESTAMP, column, text
from .database import Base
from sqlalchemy.orm import relationship


#every model (class) in this file represents a table. each class(model) is going to create a table within postgres
class Post(Base):
    #we can choose a name for our table within postgres. but the name of the class itself is just within python
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # The reason that we added property below is that when we retrieve a post, we don't wanna just see the owner_id of the user
    #  who has created the post, because it doesn't help us a lot. nobody knows who really that person is with that id
    # so it is much better to embed the user email, username, created_at time of the user. so for that we need to fetch all of 
    # that information bassed off of the relationship that this model(table) has with other tables. so here Post table has relationship
    # with User table through 'owner_id' and sqlalchemy will automatically know that using below line of code. so in this way 
    # we can fetch all the information about the user who has created the post through therelationship between these two tables.
    owner = relationship('User')

#SQLAlchemy Model for users table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__='votes'

    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True) 