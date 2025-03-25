#!/bin/bash

export $(cat .env | xargs)

# Overrides for host-specific use
export POSTGRES_PASSWORD=./db_password.txt
export DATABASE_HOST=localhost
