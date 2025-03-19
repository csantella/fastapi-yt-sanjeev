#!/bin/bash

if [[ "$0" != "./start-pgadmin4-docker.sh" ]]; then
    echo "This script must be run from within the project folder"
    echo "Dolla 0: $0"
    exit 1
fi

PGADMIN_DEFAULT_PASSWORD="$(cat .env-secret)"

docker pull dpage/pgadmin4:latest

docker run -p 5050:80 \
	-e "PGADMIN_DEFAULT_EMAIL=santella.chris@gmail.com" \
	-e "PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD" \
    -v $HOME/.volumes/pgadmin:/var/lib/pgadmin \
	--name local-pgadmin \
	-d dpage/pgadmin4
