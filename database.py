from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
#postgresql://airobo_user:tcLr3o0k6KRqhdni3FdBZuxe8WaRUJjG@dpg-ctctk7i3esus73bmf9r0-a/airobo
#sql_database_url="postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
sql_database_url="postgresql://airobo_user:tcLr3o0k6KRqhdni3FdBZuxe8WaRUJjG@dpg-ctctk7i3esus73bmf9r0-a.oregon-postgres.render.com/airobo"


engine = create_engine(sql_database_url)

seesionlocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base= declarative_base()

def get_db():
    db=seesionlocal()
    try:
        yield db
    finally:
        db.close()