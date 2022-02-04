# Open loi- Database

## Introduction
This is the database for the open loi project

## How to start

To start, first place yourself in the db/ folder and start the database with :

```
$ docker build -t postgres_fr .
$ docker-compose -f docker-compose.yml up postgres -c 'config_file=postgresql.conf'

docker run --name=postgres -p 5432:5432 -v postgres-volume:/var/lib/postgresql/data -e POSTGRES_PASSWORD=password postgres
docker exec -it postgres psql -U postgres



```

The server should start on http://localhost:8080 by default.


https://hub.docker.com/_/postgres
--shm-size=256MB
sudo ss -lptn 'sport = :5432'