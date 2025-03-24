#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPTDIR
export GIT_COMMIT_HASH=$(git rev-parse --short HEAD)
docker compose build
if [[ $? -ne 0 ]]; then
  echo "ERROR: Docker Compose Build failed."
fi

exit 0
