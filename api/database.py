from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DB_URL = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
SQLALCHEMY_DB_URL = 'postgresql+psycopg://postgres:postgres@db:5432/fastapi-yt-sanjeev'


engine = create_engine(SQLALCHEMY_DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()