# FastAPI Tutorial

## Instructions
To (re-)build all of the containers:
  `./build-all.sh`

### Helpful Aliases
  `source ./setup-alias.sh`

Then, to run the application, simply type:
  `up`

To tear down the application, type:
  `down`

To view logs for the app or db, run:
  `log_app` or
  `log_db`


## Application Information
The app runs on port `8000`, the database runs on port `5432`, and the included pgAdmin container runs on port `5050`.


## Manual App Deployment
### Running the Application
To run the application, simply run the docker-compose command below:
  ```docker compose up -d```

### Logging
To view application STDOUT, STDERR from any terminal, connect to the container's log:
 - App container: ```docker container logs -f fastapi-yt-sanjeev-app-1```
 - DB container:  ```docker container logs -f fastapi-yt-sanjeev-db-1```

### Teardown
To stop the application, run:
  `docker compose down`

The docker-compose.yml file contains the configuration for the application container and the postgres container.

### pgAdmin 4 Connection
To connect a local pgAdmin 4 Docker container to the app network, run the following commands:
  `docker network connect fastapi-yt-sanjeev_default <pgAdmin4 container name>`

where 'fastapi-yt-sanjeev_default' is the name of the docker network given to it by docker compose (since it is not explicitly defined in the YAML)
