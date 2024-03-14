README.txt

FastAPI Tutorial


To build the Docker image:

  > docker build -t fastapi_tut:latest $(PWD)


To run the Docker container:

  > docker run --name fastapi_c -v ./api:/app -dp 8000:8000 fastapi_tut:latest


To run the PostgreSQL Docker container:

  > docker run --hostname=4073bf02bd4a --env=POSTGRES_PASSWORD=postgres --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/postgresql/16/bin --env=GOSU_VERSION=1.17 --env=LANG=en_US.utf8 --env=PG_MAJOR=16 --env=PG_VERSION=16.2-1.pgdg120+2 --env=PGDATA=/var/lib/postgresql/data --volume=/var/lib/postgresql/data -p 5432:5432 --restart=no --runtime=runc -d postgres:16.2-bookworm
