README.txt

FastAPI Tutorial


To build the Docker image:

  > docker build -t fastapi_tut:latest $(PWD)


To run the Docker container:

  > docker run --name fastapi_c -v ./api:/app -dp 8000:8000 fastapi_tut:latest
