from pydantic import BaseModel,EmailStr
class post(BaseModel):
    title: str
    content: str
    published: bool = True # this is default value
    
class res_post(BaseModel):
    title: str
    content: str
    published: bool = True # this is default value
    class config:
        orm=True
    

class User(BaseModel):
    email:EmailStr
    password:str
    username:str
class res_user(BaseModel):
    email:EmailStr
    username:str
    class config:
        orm=True

class Inquirey(BaseModel):
    name:str
    email:EmailStr
    subject:str
    message:str

class Job(Inquirey):
    resume:bytes