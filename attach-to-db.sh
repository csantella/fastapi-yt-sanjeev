#!/bin/bash

(return 0 2>/dev/null) && sourced=1 || sourced=0

if [ $sourced -eq 1 ]; then
    docker container attach --sig-proxy=false fastapi-yt-sanjeev-db-1
    exit 0
else
    echo "ERROR: Script needs to be sourced."
    echo "Run as: . $0 or source $0"
    exit 1
fi
