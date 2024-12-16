from database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,LargeBinary
from sqlalchemy.sql.expression import null

class post(Base):
    __tablename__ = 'posts'

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,default=True)
    created_at=Column(TIMESTAMP(timezone=True),
                      nullable=False,server_default=text('now()'))
    
class user(Base):
    __tablename__='users'

    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    username=Column(String,primary_key=True,nullable=False)

class inquirey(Base):
    __tablename__='inquirey'
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    subject=Column(String,nullable=False)
    message=Column(String,nullable=False)

class UserApplication(Base):
    __tablename__ = "user_applications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    cover_page = Column(String, nullable=False)
    resume_filename = Column(String, nullable=False)
    resume_data = Column(LargeBinary, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),
                      nullable=False,server_default=text('now()'))
 

    