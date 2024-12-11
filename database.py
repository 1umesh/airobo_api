from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#sql_database_url="postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
sql_database_url="postgresql://postgres:sahil@localhost:5433/fastapi"

engine = create_engine(sql_database_url)

seesionlocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base= declarative_base()

def get_db():
    db=seesionlocal()
    try:
        yield db
    finally:
        db.close()