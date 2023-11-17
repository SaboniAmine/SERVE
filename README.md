# Bloom SERVE

To have a running local database, here are the steps to follow : 
- Install dependencies from the `pyproject.toml`file
- From the `docker` folder, run `docker compose up` to run db & pgadmin containers
- From the project root, run `alembic upgrade head` to apply all migrations and have the schema populating the local db.
Some env variables will need to be exported : 
```
export POSTGRES_HOSTNAME=serve
export POSTGRES_DB=serve
export POSTGRES_PASSWORD=bloom
export POSTGRES_USER=bloom_user
export POSTGRES_PORT=5480
```