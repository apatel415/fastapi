from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func
from sqlalchemy.sql.functions import current_date, current_user
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    
    # if you want to get all posts of the user only
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # **post.dict() unpacks the post dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    # if you to restrict user to retrieve only posts they made
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authrorized to perform requested action")
        
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    post_query = db.query(models.Post).filter(models.Post.id == id) # query language
    post = post_query.first() # applies the query and returns the data
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authrorized to perform requested action")
        
    post_query.delete(synchronize_session=False) # appends a delete to the original query to delete
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s
    #                where id = %s returning *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")
    # return {'data': updated_post}
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authrorized to perform requested action")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()