from models import user,inquirey,job
import models
from schemas import User,res_user,Inquirey,Job
from fastapi import Depends,HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import engine, seesionlocal,get_db
from schemas import res_user,User
from passlib.context import CryptContext


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
router=APIRouter(
    prefix="/users"
)



@router.get('/{username}', tags=["users"], response_model=res_user)
def get_user(username:str,db:Session=Depends(get_db)):
    user=db.query(models.user).filter(models.user.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user


@router.post("/", tags=["users"],status_code=status.HTTP_201_CREATED,response_model=res_user)
def create_user(user:User,db:Session=Depends(get_db)):
    
    #hash the password- User.password
    hashed=pwd_context.hash(user.password)
    user.password=hashed

    new_user=models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/send_inquirey", tags=["send"])
def send_inquirey(msg:Inquirey,db:Session=Depends(get_db)):
    new_inquirey=models.inquirey(**msg.dict())
    db.add(new_inquirey)
    db.commit()

    return {"message":"send successfully"}

@router.post("/send_resume", tags=["users"])
def send_inquirey(msg:Job,db:Session=Depends(get_db)):
    new_inquirey=models.job(**msg.dict())
    db.add(new_inquirey)
    db.commit()

    return {"message":"send successfully"}