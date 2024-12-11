from fastapi import FastAPI, Depends, HTTPException,Response,status
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from models import post,user
from database import engine, seesionlocal,get_db
from sqlalchemy.orm import Session
from schemas import post,res_post,User
models.Base.metadata.create_all(bind=engine)

app=FastAPI()


# while True:
#     try: 
#         conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres'
#                             ,password='sahil',port=5433,cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection is successfull")
#         break
#     except Exception as error:
#         print("there is some error :" ,error)
#         time.sleep(2)

''' why we need schemas :
the client can send whatever data they want
data isn't getting vaildate 
we want to force the client to send the data in a schema that we expect

And to stop all this we use pydantic
it is used to define schema '''




  
#post -> create
#get -> read
#put -> update
#delete -> delete
@app.get("/sql")
def test_db(db:Session=Depends(get_db)):
    post=db.query(models.post).all()
    return{"status":post}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts(db:Session=Depends(get_db),response_model=res_post):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # print(posts)
    post=db.query(models.post).all()
    return  post

@app.get("/posts/{id}")
#this path parameter will always be pass as string
def get_post(id: int,db:Session=Depends(get_db),response_model=res_post):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    # one_post=cursor.fetchone()
    post=db.query(models.post).filter(models.post.id==id).first()
    db.add(post)
    db.commit()
    db.refresh(post)
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id}")
    
    return post


@app.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=res_post)
def create_post(new_post: post,db:Session=Depends(get_db)):

    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(new_post.title,new_post.content,new_post.published))
    # ne_post=cursor.fetchone()
    # conn.commit()
    #we can also use new_post.dict() this will convert new_post data into a python dict
    
    ne_post=models.post(**new_post.dict())
    db.add(ne_post)
    db.commit()
    db.refresh(ne_post)
    return ne_post



#now what this post do this takes the input from user
#and send it to api.when can store this input in database 
#or print it on console or show back to user in above example
#to do all this we have store input data in variable like previous example
# but in this we didn't did all that and just returning 
#simple message back to user.

@app.delete("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int,db:Session=Depends(get_db),response_model=res_post):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    del_post=db.query(models.post).filter(models.post.id ==id )
    deleted_post=del_post.first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not found")
    del_post.delete()
    db.commit()

    return deleted_post

@app.put("/posts/{id}")
def update_item(id: int,post:post,db:Session=Depends(get_db),response_model=res_post):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s,published=%s
    #                WHERE id= %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # update_post =cursor.fetchone()
    # conn.commit()
    up_post=db.query(models.post).filter(models.post.id ==id )
    update_post=up_post.first()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not found")
    up_post.update(post.dict())
    db.commit()
    return update_post


