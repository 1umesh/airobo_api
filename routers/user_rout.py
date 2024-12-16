from models import user,inquirey
import models
from schemas import User,res_user,Inquirey,Job
from fastapi import Depends,HTTPException, status, APIRouter, File ,Form, UploadFile
from sqlalchemy.orm import Session
from database import engine, seesionlocal,get_db
from schemas import res_user,User
from passlib.context import CryptContext
import aiofiles
from PyPDF2 import PdfReader


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

@router.post("/send_resume", tags=["send"])
async def submit_application(
    name: str = Form(...),
    email: str = Form(...),
    cover_page: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)):
    # Validate file type
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Resume must be a PDF file")

    # Read the resume file content
    resume_data = await resume.read()
    resume_filename = resume.filename
    
    try:
        reader = PdfReader(resume.file)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


    # Save data to the database
    user_application = models.UserApplication(
        name=name,
        email=email,
        cover_page=cover_page,
        resume_filename=resume_text,
        resume_data=resume_data,
    )
    db.add(user_application)
    db.commit()
    db.refresh(user_application)

    return {"message": "Application submitted successfully"}

    