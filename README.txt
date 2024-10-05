README.txt

FastAPI Tutorial


To run the application, simply run the docker-compose command below:

	`docker compose up -d`


To view application STDOUT, STDERR from any terminal, connect to the container's log:

	App container: `docker container logs -f fastapi-yt-sanjeev-app-1`
	 DB container: `docker container logs -f fastapi-yt-sanjeev-db-1`


To stop the application, run:
	
	`docker compose down`


The docker-compose.yml file contains the configuration for the application container and the postgres container.

