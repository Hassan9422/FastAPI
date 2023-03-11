# from anyio import current_effective_deadline
from httpx import post
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas
from app import oauth2, utils
from ..database import engine, get_db
from typing import List, Optional

router = APIRouter(
    prefix='/posts', tags=['Posts']
)

@router.get("/{id}", response_model=schemas.Post_Out)
def Get_One_Post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # c.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id), ))
    # desired_Post = c.fetchone()

    desired_Post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()

    if not desired_Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id={id} doesn't exist")
    # conn.commit()

    # if we wanna get just the posts of the looed in user, we have to add two lines below.

    # if desired_Post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you are not allowed to see this post!')

    return desired_Post


@router.get("/", response_model=list[schemas.Post_Out])
#  in order to adding query parameters to filter the results of a request(which here it is get all posts request) based on that,
#  we have to add those parameters here as arguments path operation function. we can add queries parameters 
# like: search, limit, skip, etc.
def Get_All_Posts(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] ='' ):
    # c.execute(""" SELECT * FROM posts """)
    # posts = c.fetchall()

    # if we wanna get just the posts of the looed in user, we have to add the line below.

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # if we wanna tell the database to take the limit number in the results, we have to add 'limit' method in line below.
    # for skipping posts, we have to add offset method like below.
    #if we wanna search based off of a specific word or something in somewhere in the content or title or etc, we just have to 
    # use a method called contains like below:
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post).all()
    # print(posts)
    # this is exact query that we wrote in postgres pgadmin using raw sql. in below, we have done the exact thing using sqlalchemy.
    # we're gonna grab the number of likes/votes for each post. so we need to join tables and also grouping the final table and
    # finally count the number of rows in each group. this way we can get the number of rows in each group which gives us 
    # exactly the number of votes for each post.

    # results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        # models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    

    # we can go ahead and add query parameters to line above to narrow down the results:
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    print(posts)

    return posts   


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
# if we wanna protect this path operation, meaning we want user to be logged in before creating a post, we have to pass 
# an extra dependency into this path operation function, like below. it will go ahead and automatically take the jwt_token from 
# this request and it will also make sure that id field is correct and then it will make sure that jwt token is valid 
# by calling verify function inside of auth.py file. and if the token is expired or there is a credential exception,
# it will return us an error in verify function inside of the auth.py file.
def Create_A_Post(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # c.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # created_post = c.fetchone()
    # conn.commit()
    print(current_user.email)
    # the reason that we add owner_id property in line below is that the value of owner_id according to posts table model in models.py 
    # can not be left empty, we know that we are going to grab the owner_id from the token, here we have current_user, so we can say 
    # current_user.id is the owner_id of the post. so we have to pass that in when we create a post, like line below.
    # so again remember we didn't pass this owner_id in the body of the post request in postman! instead we grabbed it 
    # from the authenticatin process, when we send our token to API, it automatically extracts our id number, so we can easily
    # go ahead and put it here when we create a post.
    created_post = models.Post(owner_id= current_user.id, **post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def Delete_A_Post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # c.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    # deleted_post = c.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
      
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id={id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this post!')
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ResponsePost)
def Update_A_Post(id: int, upost: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # c.execute(""" UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %s RETURNING *  """,
    #                     (post.title, post.content, post.published, str(id)))

    # updated_post = c.fetchone()        
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id={id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this post!')

    post_query.update(upost.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()
