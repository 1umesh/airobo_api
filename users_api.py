from fastapi import FastAPI, Depends, HTTPException,Response,status
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from passlib.context import CryptContext
import models
from models import user
from database import engine, seesionlocal,get_db
from sqlalchemy.orm import Session
from schemas import res_user,User
from routers import user_rout

models.Base.metadata.create_all(bind=engine)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

app=FastAPI()
app.include_router(user_rout.router)


@app.get("/")
def test_db(db:Session=Depends(get_db)):
    users=db.query(models.user).all()
    return{"status":users}

