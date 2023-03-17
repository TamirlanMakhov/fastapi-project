from fastapi_cache.decorator import cache

from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, HTTPException, Depends, APIRouter, Query, Request, Response
from ..database import get_db


router = APIRouter(prefix='/posts', tags=['Posts'])


@cache(expire=60)
@router.get('/', response_model=list[schemas.PostVote])
def get_posts(request: Request, response: Response, db: Session = Depends(get_db),
              current_user=Depends(oauth2.auth_handler.get_current_user),
              limit: int = Query(default=10, title='limit', description='how many items to show'),
              skip: int = Query(default=0, title='skip', description='how many items to skip'),
              search: str | None = Query(default="", title='search string', description='search pattern')):
    posts = db.query(models.Post, func.count(models.Vote.post_id)
                     .label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.auth_handler.get_current_user)):
    """user should be login before he can create posts, so user_id is dependency"""

    created_post = models.Post(**post.dict(), owner_id=current_user.id)

    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post


@router.get("/{my_id}", response_model=schemas.PostVote)
def get_post_by_id(my_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.auth_handler.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id)
                     .label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id).filter(models.Post.id == my_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post id <{my_id}> wasn't found")
    return posts


@router.delete("/{my_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(my_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.auth_handler.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == my_id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {my_id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'not authorised to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{my_id}", response_model=schemas.Post)
def update_post(my_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.auth_handler.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == my_id)
    actual_post = post_query.first()

    if not actual_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {my_id} does not exist")
    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'not authorised to perform requested action')

    post_query.update(post.dict())
    db.commit()

    return post_query.first()




# raw sql
# @app.get("/posts/{my_id}")
# def get_post(my_id: int):
#     cursor.execute("""SELECT * FROM POSTS
#                               WHERE id = %s""", (str(my_id),))
#     result = cursor.fetchone()
#
#     if not result:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post id <{my_id}> wasn't found")
#
#     return {"post_detail": result}

# raw sql
# @app.get("/posts")
# def get_posts():
#     try:
#         cursor.execute("""SELECT * FROM posts;""")
#         posts = cursor.fetchall()
#         return {"data": posts}
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no content")


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published)
#                       values (%s, %s, %s) RETURNING *""",
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


# @app.delete("/posts/{my_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(my_id: int):
#     cursor.execute("""DELETE FROM posts
#                       WHERE ID = %s returning * """, (str(my_id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {my_id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{my_id}")
# def update_post(my_id: int, post: Post):
#     cursor.execute("""UPDATE posts
#                       SET title = %s, content = %s, published = %s
#                       WHERE id = %s returning *""", (post.title, post.content, post.published, str(my_id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {my_id} does not exist")
#     return {"data": updated_post}
