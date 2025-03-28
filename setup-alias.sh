alias up="docker compose up -d"
alias down="docker compose down"
alias log_app="docker container logs --follow fastapi-yt-sanjeev-app-1"
alias log_db="docker container logs --follow fastapi-yt-sanjeev-db-1"
alias log_pgadmin="docker container logs --follow fastapi-yt-sanjeev-pgadmin-1"
alias connect_pgadmin="docker network connect fastapi-yt-sanjeev_default local-pgadmin"
