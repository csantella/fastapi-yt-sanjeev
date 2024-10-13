import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = [ "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_USER" ]


# Sanity check for presence of all required env variables
exit_flag = False
for var in env:
    print(f"{var} = {os.environ[var]}")
    if os.environ[var] == "":
        print(f"(!) Error, {var} is empty.", flush=True)
        exit_flag = True

if exit_flag:
    exit(1)


try:
    with open(os.environ["POSTGRES_PASSWORD"], 'r') as db_pass_file:
        POSTGRES_PASSWORD = next(db_pass_file).strip()
except OSError:
    print(f"Unable to open postgres password secret at {os.environ["POSTGRES_PASSWORD"]}")
    exit(1)


# SQLALCHEMY_DB_URL = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
#SQLALCHEMY_DB_URL = 'postgresql+psycopg://postgres:postgres@db:5432/fastapi-yt-sanjeev'
SQLALCHEMY_DB_URL = "postgresql+psycopg://{}:{}@{}:5432/fastapi-yt-sanjeev".format(
    os.environ["POSTGRES_USER"],
    POSTGRES_PASSWORD,
    os.environ["POSTGRES_HOST"],
    os.environ["POSTGRES_USER"])

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