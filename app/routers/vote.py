from fastapi import FastAPI, Query, status, Response, HTTPException, Depends, APIRouter
# the reason that we have imported oath2 in line below is that we wanna make sure that the user has logged in before voting for a post.
from .. import models, database, schemas, oauth2
from sqlalchemy.orm import Session

# in this file we're gonna set the logic fro voting a specific post. there are some things that we have to make sure 
# we have considered them. first, when we send a request to vote for a post from postman, we don't need to send user_id 
# in body of the request, because we can grab it from jwt token when the user logs in. but we need to send two things in body 
# of the request. id of the post that we wanna vote or like and the direction of the vote(meaning if the direction is 0, we wanna remove the vote
#  and if the direction is 1, we wanna vote/like the post. because sometimes, we accidently like/vote for a post and we wanna 
# remove the like, so we need tto have the possiblity of removing the post.)

router = APIRouter(
    prefix='/vote', tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
# so we need to pass several things as arguments to this path operation function to make the logic of vote/ like system.
# keep in mind that like some other routes, because we ask the user to provide some data in the body, it means that we have to 
# define a schema, so make sure that the user has provided the correct data. so we gotta define a schema for vote in schemas.py file.
# 
# in below, we set up schema nad also database(to make queries) as we did for other routes. once we get all the required dependencies
# like below, we can go ahead and define our logic.
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # so first of all, we're gonna query the database to see whether the requested post is existed or not, if it exists,
    # we check two different scenarios in which an HTTPException can happen: 1) if the user wants to vote for a post 
    # which already ha been voted by the same user. 2) if the user wants to remove a post and the post doesn't even exit in database
    # in this situation also there is an HTTPException.
    # but if the requsted post exists in database and we have none of the two scnarios in above, we will go ahead and perform the
    # requested action which can be either deletion or creation of a vote for a particular post.


    # but first we gotta keeep in mind that it is likely that user tries to pass a post_id that doesn't even exist! 
    # so in this case we have to raise an exception saying that the post doesn't exist:
    Query1 = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if  not Query1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with the id={vote.post_id} doesn't exist")
    


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    print(found_vote, type(found_vote))
    # if not db.query(models.Vote).filter(models.Vote.post_id == vote.post_id):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the post dosen't exist!")
    

    if vote.dir == 1:
        # here we wanna check whether the user has already voted for the post or not. if he has, we will raise 
        # an exception like following
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'the post with the id={vote.post_id} is voted already')
        
        # if the user hasn't voted for the post already, we go ahead and create a brand new vote in Vote table.
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        # print(new_vote)
        db.add(new_vote)
        db.commit()
        return f'you voted for the post with the id ={vote.post_id} successfully'
        # the following is the logic for the case that user wants to removes a vote/like
    else:
        # here like above first we check for a situation where a exception can be raised. and that is when the post already doesn't 
        # exist or it has been deleted! in this case the user is not able to delete a vote for a post that has been deleted
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"you haven't voted for the post with id={vote.post_id}")
        # if the post exists, we easily go ahead and delete the requested post that is avalable in the database.
        vote_query.delete(synchronize_session = False)
        db.commit()
        return f'The vote for post with id={vote.post_id} successfully got deleted'
    