from fastapi import status, HTTPException, Depends, APIRouter, FastAPI
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(current_vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user=Depends(oauth2.auth_handler.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == current_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {current_vote.post_id} does '
                                                                          f'not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == current_vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if current_vote.dir:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted '
                                                                             f'on post {current_vote.post_id}')
        new_vote = models.Vote(post_id=current_vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote does not exist')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "vote was deleted"}
