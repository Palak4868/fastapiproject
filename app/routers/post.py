from .. import models,schemas,utlis
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from ..import models,schemas,oauth2
from sqlalchemy import func


router=APIRouter( prefix= "/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip :int = 0, search:Optional[str]=""):

    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()
    #print(limit)
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #old sql logic 

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """ , (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    
    #new sqlalchemy logic 
    #new_post=models.Post(title=post.title, content = post.content, published=post.published)
    #using unpacking dictionary way for much more cleaner and better
    
    
    #print(current_user.email) 
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#getting one post 
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db:Session=Depends(get_db), current_user : int = Depends(oauth2.get_current_user)): #response:Response 
    
    #old sql logic
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s""", (str(id),))
    # post=cursor.fetchone()
    # print(test_post)
    # post=find_post(id)

    #new sqlalchemy logic 
    #post=db.query(models.Post).filter(models.Post.id == id).first()

    #new post query with votes
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

   # print(post)
       
    if not post:
        #METHOD 1 (using Response)
        #response.status_code=404
        #METHOD 2 (Using status)
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id: {id} was not found"}
        #METHOD 3 (Using HTTP Exception)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} was not found")

    return post


#deleting a post 
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):


    #old sql logic
    #cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING * """,(str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()


   # index=find_index_post(id)

   #new sqlalchemy logic 
   post_query=db.query(models.Post).filter(models.Post.id==id)
   post=post_query.first()
   
   if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist")
   
   if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform required action")
   

    #my_posts.pop(index)
   # return {'message' : "post was successfully deleted"}

   post_query.delete(synchronize_session= False)
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)

#updating a post 
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    #old sql logic
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published,str(id)))
#     updated_post=cursor.fetchone()
#     conn.commit()


    # index = find_index_post(id)


    #new sqlalchemy logic 
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform required action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index] = post_dict

    return post_query.first()


