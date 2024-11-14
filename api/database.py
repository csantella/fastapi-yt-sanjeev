import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


try:
    with open(os.environ["POSTGRES_PASSWORD"], 'r') as db_pass_file:
        settings.database_password = next(db_pass_file).strip()
except OSError:
    print(f"Unable to open postgres password secret at {settings.database_password}")
    exit(1)


# SQLALCHEMY_DB_URL = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
#SQLALCHEMY_DB_URL = 'postgresql+psycopg://postgres:postgres@db:5432/fastapi-yt-sanjeev'
SQLALCHEMY_DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
    settings.database_username,
    settings.database_password,
    settings.database_host,
    settings.database_port,
    settings.database_name)

#print(f"{SQLALCHEMY_DB_URL:}")


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